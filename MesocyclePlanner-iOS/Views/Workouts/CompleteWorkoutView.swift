//
//  CompleteWorkoutView.swift
//  MesocyclePlanner
//

import SwiftUI

struct CompleteWorkoutView: View {
    let workout: Workout
    @ObservedObject var workoutService: WorkoutService
    let onComplete: () -> Void
    
    @Environment(\.dismiss) var dismiss
    
    @State private var durationMinutes: String = ""
    @State private var notes: String = ""
    
    var body: some View {
        NavigationStack {
            Form {
                Section("Workout Summary") {
                    HStack {
                        Text("Workout")
                        Spacer()
                        Text(workout.name)
                            .foregroundColor(.secondary)
                    }
                    
                    HStack {
                        Text("Scheduled")
                        Spacer()
                        Text(workout.scheduledDate, style: .date)
                            .foregroundColor(.secondary)
                    }
                }
                
                Section("Completion Details") {
                    HStack {
                        Text("Duration")
                        Spacer()
                        TextField("Minutes", text: $durationMinutes)
                            .keyboardType(.numberPad)
                            .multilineTextAlignment(.trailing)
                            .frame(width: 80)
                        Text("min")
                            .foregroundColor(.secondary)
                    }
                }
                
                Section("Notes") {
                    TextEditor(text: $notes)
                        .frame(height: 120)
                }
                
                Section {
                    Text("How did it feel?")
                        .font(AppTypography.caption)
                        .foregroundColor(.secondary)
                    
                    TextEditor(text: $notes)
                        .frame(height: 80)
                }
            }
            .navigationTitle("Complete Workout")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") {
                        dismiss()
                    }
                }
                
                ToolbarItem(placement: .confirmationAction) {
                    Button("Complete") {
                        Task {
                            await completeWorkout()
                        }
                    }
                }
            }
        }
    }
    
    private func completeWorkout() async {
        let duration = Int(durationMinutes)
        let workoutNotes = notes.isEmpty ? nil : notes
        
        let success = await workoutService.completeWorkout(
            id: workout.id,
            durationMinutes: duration,
            notes: workoutNotes
        )
        
        if success {
            dismiss()
            onComplete()
        }
    }
}

#Preview {
    CompleteWorkoutView(
        workout: Workout(
            id: UUID(),
            mesocycleId: UUID(),
            name: "Upper Body Push",
            scheduledDate: Date(),
            completed: false,
            createdAt: Date(),
            updatedAt: Date()
        ),
        workoutService: WorkoutService(),
        onComplete: {}
    )
}
