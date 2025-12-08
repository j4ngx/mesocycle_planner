//
//  MainTabView.swift
//  MesocyclePlanner
//

import SwiftUI

struct MainTabView: View {
    @State private var selectedTab = 0
    
    var body: some View {
        TabView(selection: $selectedTab) {
            HomeView()
                .tabItem {
                    Label("Home", systemImage: "house.fill")
                }
                .tag(0)
            
            ExerciseLibraryView()
                .tabItem {
                    Label("Exercises", systemImage: "figure.strengthtraining.traditional")
                }
                .tag(1)
            
            MesocycleListView()
                .tabItem {
                    Label("Mesocycles", systemImage: "calendar")
                }
                .tag(2)
            
            WorkoutListView()
                .tabItem {
                    Label("Workouts", systemImage: "dumbbell.fill")
                }
                .tag(3)
            
            ProfileView()
                .tabItem {
                    Label("Profile", systemImage: "person.fill")
                }
                .tag(4)
        }
        .tint(AppColors.primary)
    }
}

struct HomeView: View {
    @EnvironmentObject var authService: AuthService
    
    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: AppSpacing.lg) {
                    // Welcome section
                    VStack(alignment: .leading, spacing: AppSpacing.sm) {
                        Text("Welcome back,")
                            .font(AppTypography.title2)
                            .foregroundColor(.secondary)
                        
                        Text(authService.currentUser?.username ?? "Athlete")
                            .font(AppTypography.largeTitle)
                            .fontWeight(.bold)
                    }
                    .padding(.horizontal)
                    
                    // Quick stats cards
                    LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: AppSpacing.md) {
                        StatCard(title: "Active Mesocycle", value: "Week 3/12", icon: "calendar", color: .blue)
                        StatCard(title: "Workouts", value: "8 this week", icon: "dumbbell.fill", color: .green)
                        StatCard(title: "Progress", value: "+2.5kg", icon: "chart.line.uptrend.xyaxis", color: .purple)
                        StatCard(title: "Streak", value: "12 days", icon: "flame.fill", color: .orange)
                    }
                    .padding(.horizontal)
                }
                .padding(.vertical)
            }
            .navigationTitle("Dashboard")
            .background(AppColors.secondaryBackground)
        }
    }
}

struct StatCard: View {
    let title: String
    let value: String
    let icon: String
    let color: Color
    
    var body: some View {
        VStack(alignment: .leading, spacing: AppSpacing.sm) {
            Image(systemName: icon)
                .font(.title2)
                .foregroundColor(color)
            
            Text(value)
                .font(AppTypography.title2)
                .fontWeight(.bold)
            
            Text(title)
                .font(AppTypography.caption)
                .foregroundColor(.secondary)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding()
        .background(AppColors.cardBackground)
        .cornerRadius(AppCornerRadius.md)
        .shadow(color: .black.opacity(0.05), radius: 5, x: 0, y: 2)
    }
}
