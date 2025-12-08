//
//  ProfileView.swift
//  MesocyclePlanner
//

import SwiftUI

struct ProfileView: View {
    @EnvironmentObject var authService: AuthService
    @State private var showLogoutAlert = false
    
    var body: some View {
        NavigationStack {
            List {
                // User info section
                Section {
                    if let user = authService.currentUser {
                        VStack(alignment: .leading, spacing: AppSpacing.sm) {
                            Text(user.username)
                                .font(AppTypography.title2)
                                .fontWeight(.bold)
                            
                            Text(user.email)
                                .font(AppTypography.body)
                                .foregroundColor(.secondary)
                            
                            HStack {
                                Image(systemName: "figure.strengthtraining.traditional")
                                    .font(.caption)
                                Text(user.trainingLevel.displayName)
                                    .font(AppTypography.caption)
                            }
                            .foregroundColor(.secondary)
                            .padding(.top, 4)
                        }
                        .padding(.vertical, AppSpacing.sm)
                    }
                }
                
                // Settings
                Section("Settings") {
                    NavigationLink {
                        Text("Edit Profile")
                    } label: {
                        Label("Edit Profile", systemImage: "person.fill")
                    }
                    
                    NavigationLink {
                        Text("Preferences")
                    } label: {
                        Label("Preferences", systemImage: "gearshape.fill")
                    }
                }
                
                // About
                Section("About") {
                    NavigationLink {
                        Text("Help & Support")
                    } label: {
                        Label("Help & Support", systemImage: "questionmark.circle.fill")
                    }
                    
                    NavigationLink {
                        Text("Privacy Policy")
                    } label: {
                        Label("Privacy Policy", systemImage: "hand.raised.fill")
                    }
                }
                
                // Logout
                Section {
                    Button(role: .destructive) {
                        showLogoutAlert = true
                    } label: {
                        HStack {
                            Spacer()
                            Label("Logout", systemImage: "rectangle.portrait.and.arrow.right")
                            Spacer()
                        }
                    }
                }
            }
            .navigationTitle("Profile")
            .alert("Logout", isPresented: $showLogoutAlert) {
                Button("Cancel", role: .cancel) {}
                Button("Logout", role: .destructive) {
                    authService.logout()
                }
            } message: {
                Text("Are you sure you want to logout?")
            }
        }
    }
}
