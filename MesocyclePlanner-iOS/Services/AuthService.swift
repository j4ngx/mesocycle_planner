//
//  AuthService.swift
//  MesocyclePlanner
//
//  Authentication service with token management
//

import Foundation
import Combine

class AuthService: ObservableObject {
    static let shared = AuthService()
    
    @Published var isAuthenticated = false
    @Published var currentUser: User?
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    private let apiClient = APIClient.shared
    private let keychainManager = KeychainManager.shared
    
    private init() {
        // Check if token exists
        if keychainManager.getToken() != nil {
            isAuthenticated = true
            Task {
                await fetchCurrentUser()
            }
        }
    }
    
    // MARK: - Login
    @MainActor
    func login(email: String, password: String) async {
        isLoading = true
        errorMessage = nil
        
        do {
            let credentials = UserLogin(email: email, password: password)
            let response: TokenResponse = try await apiClient.request(
                endpoint: "/auth/login",
                method: .post,
                body: credentials,
                requiresAuth: false
            )
            
            // Save token
            keychainManager.saveToken(response.accessToken)
            
            // Fetch user data
            await fetchCurrentUser()
            
            isAuthenticated = true
            isLoading = false
        } catch {
            errorMessage = error.localizedDescription
            isLoading = false
        }
    }
    
    // MARK: - Register
    @MainActor
    func register(email: String, username: String, password: String, fullName: String?, trainingLevel: TrainingLevel) async {
        isLoading = true
        errorMessage = nil
        
        do {
            let userData = UserCreate(
                email: email,
                username: username,
                password: password,
                fullName: fullName,
                trainingLevel: trainingLevel
            )
            
            let response: TokenResponse = try await apiClient.request(
                endpoint: "/auth/register",
                method: .post,
                body: userData,
                requiresAuth: false
            )
            
            // Save token
            keychainManager.saveToken(response.accessToken)
            
            // Fetch user data
            await fetchCurrentUser()
            
            isAuthenticated = true
            isLoading = false
        } catch {
            errorMessage = error.localizedDescription
            isLoading = false
        }
    }
    
    // MARK: - Fetch Current User
    @MainActor
    func fetchCurrentUser() async {
        do {
            let user: User = try await apiClient.request(endpoint: "/users/me")
            currentUser = user
        } catch {
            // If fetching user fails, logout
            logout()
        }
    }
    
    // MARK: - Logout
    @MainActor
    func logout() {
        keychainManager.deleteToken()
        currentUser = nil
        isAuthenticated = false
    }
    
    // MARK: - Update Profile
    @MainActor
    func updateProfile(username: String?, fullName: String?, trainingLevel: TrainingLevel?) async {
        isLoading = true
        errorMessage = nil
        
        do {
            struct UpdateRequest: Codable {
                var username: String?
                var fullName: String?
                var trainingLevel: TrainingLevel?
            }
            
            let updateData = UpdateRequest(
                username: username,
                fullName: fullName,
                trainingLevel: trainingLevel
            )
            
            let updatedUser: User = try await apiClient.request(
                endpoint: "/users/me",
                method: .put,
                body: updateData
            )
            
            currentUser = updatedUser
            isLoading = false
        } catch {
            errorMessage = error.localizedDescription
            isLoading = false
        }
    }
}
