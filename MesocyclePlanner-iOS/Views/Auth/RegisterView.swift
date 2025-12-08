//
//  RegisterView.swift
//  MesocyclePlanner
//

import SwiftUI

struct RegisterView: View {
    @Environment(\.dismiss) var dismiss
    @EnvironmentObject var authService: AuthService
    
    @State private var email = ""
    @State private var username = ""
    @State private var password = ""
    @State private var fullName = ""
    @State private var selectedLevel: TrainingLevel = .intermediate
    
    var body: some View {
        NavigationStack {
            Form {
                Section("Account Information") {
                    TextField("Email", text: $email)
                        .textInputAutocapitalization(.never)
                        .keyboardType(.emailAddress)
                    
                    TextField("Username", text: $username)
                        .textInputAutocapitalization(.never)
                    
                    SecureField("Password", text: $password)
                }
                
                Section("Personal Information") {
                    TextField("Full Name (Optional)", text: $fullName)
                    
                    Picker("Training Level", selection: $selectedLevel) {
                        ForEach(TrainingLevel.allCases, id: \.self) { level in
                            Text(level.displayName).tag(level)
                        }
                    }
                }
                
                if let error = authService.errorMessage {
                    Section {
                        Text(error)
                            .foregroundColor(AppColors.error)
                            .font(AppTypography.caption)
                    }
                }
                
                Section {
                    PrimaryButton(
                        title: "Create Account",
                        isLoading: authService.isLoading
                    ) {
                        Task {
                            await authService.register(
                                email: email,
                                username: username,
                                password: password,
                                fullName: fullName.isEmpty ? nil : fullName,
                                trainingLevel: selectedLevel
                            )
                            if authService.isAuthenticated {
                                dismiss()
                            }
                        }
                    }
                }
            }
            .navigationTitle("Sign Up")
            .navigationBarTitleDisplayMode(.large)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") {
                        dismiss()
                    }
                }
            }
        }
    }
}
