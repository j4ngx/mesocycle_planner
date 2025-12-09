//
//  WorkoutDetailView.swift
//  MesocyclePlanner
//

import SwiftUI

struct WorkoutDetailView: View {
    let workout: Workout
    @StateObject private var workoutService = WorkoutService()
    @State private var showCompleteSheet = false
    @Environment(\.dismiss) var dismiss
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: AppSpacing.lg) {
                // Header Card
                VStack(alignment: .leading, spacing: AppSpacing.md) {
                    HStack {
                        VStack(alignment: .leading, spacing: 4) {
                            Text(workout.name)
                                .font(AppTypography.title)
                                .fontWeight(.bold)
                            
                            if let split = workout.split {
                                Text(split.displayName)
                                    .font(AppTypography.subheadline)
                                    .foregroundColor(.secondary)
                            }
                        }
                        
                        Spacer()
                        
                        if workout.completed {
                            Image(systemName: "checkmark.circle.fill")
                                .font(.title)
                                .foregroundColor(.green)
                        }
                    }
                    
                    Divider()
                    
                    // Workout Info
                    VStack(spacing: AppSpacing.sm) {
                        InfoRow(icon: "calendar", label: "Scheduled", value: workout.scheduledDate.formatted(date: .abbreviated, time: .shortened))
                        
                        if workout.completed, let completedAt = workout.completedAt {
                            InfoRow(icon: "checkmark.circle", label: "Completed", value: completedAt.formatted(date: .abbreviated, time: .shortened))
                        }
                        
                        if let duration = workout.durationMinutes {
                            InfoRow(icon: "timer", label: "Duration", value: "\(duration) minutes")
                        }
                    }
                }
                .padding()
                .background(AppColors.cardBackground)
                .cornerRadius(AppCornerRadius.md)
                
                // Description
                if let description = workout.description {
                    VStack(alignment: .leading, spacing: AppSpacing.sm) {
                        Text("Description")
                            .font(AppTypography.headline)
                            .fontWeight(.semibold)
                        
                        Text(description)
                            .font(AppTypography.body)
                            .foregroundColor(.secondary)
                    }
                    .padding()
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .background(AppColors.cardBackground)
                    .cornerRadius(AppCornerRadius.md)
                }
                
                // Notes
                if let notes = workout.notes {
                    VStack(alignment: .leading, spacing: AppSpacing.sm) {
                        Text("Notes")
                            .font(AppTypography.headline)
                            .fontWeight(.semibold)
                        
                        Text(notes)
                            .font(AppTypography.body)
                            .foregroundColor(.secondary)
                    }
                    .padding()
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .background(AppColors.cardBackground)
                    .cornerRadius(AppCornerRadius.md)
                }
                
                // Action Buttons
                if !workout.completed {
                    VStack(spacing: AppSpacing.md) {
                        Button {
                            showCompleteSheet = true
                        } label: {
                            Label("Complete Workout", systemImage: "checkmark.circle.fill")
                                .font(AppTypography.headline)
                                .frame(maxWidth: .infinity)
                                .padding()
                                .background(AppColors.primary)
                                .foregroundColor(.white)
                                .cornerRadius(AppCornerRadius.md)
                        }
                        
                        Button(role: .destructive) {
                            Task {
                                let success = await workoutService.deleteWorkout(id: workout.id)
                                if success {
                                    dismiss()
                                }
                            }
                        } label: {
                            Label("Delete Workout", systemImage: "trash")
                                .font(AppTypography.headline)
                                .frame(maxWidth: .infinity)
                                .padding()
                                .background(Color.red.opacity(0.1))
                                .foregroundColor(.red)
                                .cornerRadius(AppCornerRadius.md)
                        }
                    }
                    .padding(.top)
                }
            }
            .padding()
        }
        .navigationBarTitleDisplayMode(.inline)
        .sheet(isPresented: $showCompleteSheet) {
            CompleteWorkoutView(workout: workout, workoutService: workoutService) {
                dismiss()
            }
        }
    }
}

struct InfoRow: View {
    let icon: String
    let label: String
    let value: String
    
    var body: some View {
        HStack {
            Image(systemName: icon)
                .foregroundColor(AppColors.primary)
                .frame(width: 20)
            
            Text(label)
                .font(AppTypography.subheadline)
                .foregroundColor(.secondary)
            
            Spacer()
            
            Text(value)
                .font(AppTypography.subheadline)
                .fontWeight(.medium)
        }
    }
}

#Preview {
    NavigationStack {
        WorkoutDetailView(workout: Workout(
            id: UUID(),
            mesocycleId: UUID(),
            name: "Upper Body Push",
            description: "Focus on chest, shoulders, and triceps",
            scheduledDate: Date(),
            completed: false,
            createdAt: Date(),
            updatedAt: Date()
        ))
    }
}
