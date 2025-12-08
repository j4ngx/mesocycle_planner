//
//  LoginView.swift
//  MesocyclePlanner
//
//  Login screen with email and password
//

import SwiftUI

struct LoginView: View {
    @EnvironmentObject var authService: AuthService
    @State private var email = ""
    @State private var password = ""
    @State private var showRegister = false
    
    var body: some View {
        NavigationStack {
            ZStack {
                // Background gradient
                LinearGradient(
                    colors: [AppColors.primary.opacity(0.3), AppColors.secondary.opacity(0.3)],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                )
                .ignoresSafeArea()
                
                VStack(spacing: AppSpacing.lg) {
                    Spacer()
                    
                    // Logo and title
                    VStack(spacing: AppSpacing.md) {
                        Image(systemName: "figure.strengthtraining.traditional")
                            .font(.system(size: 80))
                            .foregroundStyle(AppColors.primary)
                        
                        Text("Mesocycle Planner")
                            .font(AppTypography.largeTitle)
                            .fontWeight(.bold)
                        
                        Text("Plan. Train. Progress.")
                            .font(AppTypography.callout)
                            .foregroundColor(.secondary)
                    }
                    .padding(.bottom, AppSpacing.xl)
                    
                    // Login form
                    VStack(spacing: AppSpacing.md) {
                        CustomTextField(
                            icon: "envelope.fill",
                            placeholder: "Email",
                            text: $email
                        )
                        .textInputAutocapitalization(.never)
                        .keyboardType(.emailAddress)
                        
                        CustomTextField(
                            icon: "lock.fill",
                            placeholder: "Password",
                            text: $password,
                            isSecure: true
                        )
                        
                        if let error = authService.errorMessage {
                            Text(error)
                                .font(AppTypography.caption)
                                .foregroundColor(AppColors.error)
                                .padding(.horizontal)
                        }
                        
                        PrimaryButton(
                            title: "Login",
                            isLoading: authService.isLoading
                        ) {
                            Task {
                                await authService.login(email: email, password: password)
                            }
                        }
                        .padding(.top, AppSpacing.sm)
                        
                        Button {
                            showRegister = true
                        } label: {
                            Text("Don't have an account? **Sign up**")
                                .font(AppTypography.callout)
                        }
                        .padding(.top, AppSpacing.sm)
                    }
                    .padding(.horizontal, AppSpacing.lg)
                    
                    Spacer()
                }
            }
            .sheet(isPresented: $showRegister) {
                RegisterView()
            }
        }
    }
}
