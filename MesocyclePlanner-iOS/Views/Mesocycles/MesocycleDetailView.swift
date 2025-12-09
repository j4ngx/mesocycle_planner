//
//  MesocycleDetailView.swift
//  MesocyclePlanner
//

import SwiftUI

struct MesocycleDetailView: View {
    let mesocycle: Mesocycle
    @StateObject private var workoutService = WorkoutService()
    
    var mesocycleWorkouts: [Workout] {
        workoutService.workouts.filter { $0.mesocycleId == mesocycle.id }
    }
    
    var completedWorkouts: Int {
        mesocycleWorkouts.filter { $0.completed }.count
    }
    
    var totalWorkouts: Int {
        mesocycleWorkouts.count
    }
    
    var progressPercentage: Double {
        guard totalWorkouts > 0 else { return 0 }
        return Double(completedWorkouts) / Double(totalWorkouts)
    }
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: AppSpacing.lg) {
                // Header Card
                VStack(alignment: .leading, spacing: AppSpacing.md) {
                    HStack {
                        VStack(alignment: .leading, spacing: 4) {
                            Text(mesocycle.name)
                                .font(AppTypography.title)
                                .fontWeight(.bold)
                            
                            Text(mesocycle.periodizationModel.displayName)
                                .font(AppTypography.subheadline)
                                .foregroundColor(.secondary)
                        }
                        
                        Spacer()
                        
                        StatusBadge(status: mesocycle.status)
                    }
                    
                    if let description = mesocycle.description {
                        Text(description)
                            .font(AppTypography.body)
                            .foregroundColor(.secondary)
                    }
                }
                .padding()
                .background(AppColors.cardBackground)
                .cornerRadius(AppCornerRadius.md)
                
                // Stats Grid
                LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: AppSpacing.md) {
                    StatCard(title: "Goal", value: mesocycle.goal.displayName, icon: mesocycle.goal.icon, color: .blue)
                    StatCard(title: "Duration", value: "\(mesocycle.durationWeeks) weeks", icon: "calendar", color: .green)
                    StatCard(title: "Frequency", value: "\(mesocycle.weeklyFrequency)x/week", icon: "repeat", color: .purple)
                    StatCard(title: "Progress", value: "\(completedWorkouts)/\(totalWorkouts)", icon: "chart.bar.fill", color: .orange)
                }
                
                // Timeline
                VStack(alignment: .leading, spacing: AppSpacing.sm) {
                    Text("Timeline")
                        .font(AppTypography.headline)
                        .fontWeight(.semibold)
                    
                    VStack(spacing: AppSpacing.sm) {
                        TimelineRow(icon: "calendar.badge.plus", label: "Start Date", value: mesocycle.startDate.formatted(date: .abbreviated, time: .omitted))
                        TimelineRow(icon: "calendar.badge.checkmark", label: "End Date", value: mesocycle.endDate.formatted(date: .abbreviated, time: .omitted))
                        TimelineRow(icon: "calendar.badge.clock", label: "Created", value: mesocycle.createdAt.formatted(date: .abbreviated, time: .omitted))
                    }
                }
                .padding()
                .background(AppColors.cardBackground)
                .cornerRadius(AppCornerRadius.md)
                
                // Deload Weeks
                if let deloadWeeks = mesocycle.deloadWeeks, !deloadWeeks.isEmpty {
                    VStack(alignment: .leading, spacing: AppSpacing.sm) {
                        Text("Deload Weeks")
                            .font(AppTypography.headline)
                            .fontWeight(.semibold)
                        
                        HStack {
                            ForEach(deloadWeeks, id: \.self) { week in
                                Text("Week \(week)")
                                    .font(AppTypography.caption)
                                    .padding(.horizontal, AppSpacing.sm)
                                    .padding(.vertical, AppSpacing.xs)
                                    .background(AppColors.primary.opacity(0.2))
                                    .foregroundColor(AppColors.primary)
                                    .cornerRadius(AppCornerRadius.sm)
                            }
                        }
                    }
                    .padding()
                    .background(AppColors.cardBackground)
                    .cornerRadius(AppCornerRadius.md)
                }
                
                // Progress Bar
                if mesocycle.status == .active {
                    VStack(alignment: .leading, spacing: AppSpacing.sm) {
                        HStack {
                            Text("Completion Progress")
                                .font(AppTypography.headline)
                                .fontWeight(.semibold)
                            
                            Spacer()
                            
                            Text("\(Int(progressPercentage * 100))%")
                                .font(AppTypography.subheadline)
                                .foregroundColor(.secondary)
                        }
                        
                        ProgressView(value: progressPercentage)
                            .tint(AppColors.primary)
                    }
                    .padding()
                    .background(AppColors.cardBackground)
                    .cornerRadius(AppCornerRadius.md)
                }
                
                // Recent Workouts
                if !mesocycleWorkouts.isEmpty {
                    VStack(alignment: .leading, spacing: AppSpacing.sm) {
                        Text("Recent Workouts")
                            .font(AppTypography.headline)
                            .fontWeight(.semibold)
                        
                        ForEach(mesocycleWorkouts.prefix(5)) { workout in
                            NavigationLink(destination: WorkoutDetailView(workout: workout)) {
                                WorkoutRow(workout: workout)
                            }
                        }
                    }
                }
            }
            .padding()
        }
        .navigationBarTitleDisplayMode(.inline)
        .task {
            await workoutService.fetchWorkouts(mesocycleId: mesocycle.id)
        }
    }
}

struct TimelineRow: View {
    let icon: String
    let label: String
    let value: String
    
    var body: some View {
        HStack {
            Image(systemName: icon)
                .foregroundColor(AppColors.primary)
                .frame(width: 24)
            
            Text(label)
                .font(AppTypography.subheadline)
                .foregroundColor(.secondary)
            
            Spacer()
            
            Text(value)
                .font(AppTypography.subheadline)
                .fontWeight(.medium)
        }
        .padding(.vertical, AppSpacing.xs)
    }
}

#Preview {
    NavigationStack {
        MesocycleDetailView(mesocycle: Mesocycle(
            id: UUID(),
            userId: UUID(),
            name: "Hypertrophy Block 1",
            description: "Focus on muscle growth with moderate intensity",
            periodizationModel: .dailyUndulating,
            goal: .hypertrophy,
            durationWeeks: 12,
            startDate: Date(),
            endDate: Calendar.current.date(byAdding: .weekOfYear, value: 12, to: Date())!,
            status: .active,
            trainingLevel: "intermediate",
            weeklyFrequency: 4,
            deloadWeeks: [4, 8, 12],
            createdAt: Date(),
            updatedAt: Date()
        ))
    }
}
