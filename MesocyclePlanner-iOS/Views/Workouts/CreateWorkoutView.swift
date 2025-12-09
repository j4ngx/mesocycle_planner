//
//  CreateWorkoutView.swift
//  MesocyclePlanner
//

import SwiftUI

struct CreateWorkoutView: View {
    @ObservedObject var workoutService: WorkoutService
    @StateObject private var mesocycleService = MesocycleService()
    @Environment(\.dismiss) var dismiss
    
    @State private var name: String = ""
    @State private var description: String = ""
    @State private var scheduledDate = Date()
    @State private var selectedMesocycle: Mesocycle?
    @State private var selectedSplit: TrainingSplit = .push
    @State private var notes: String = ""
    
    var body: some View {
        NavigationStack {
            Form {
                Section("Workout Details") {
                    TextField("Name", text: $name)
                    
                    Picker("Training Split", selection: $selectedSplit) {
                        ForEach(TrainingSplit.allCases, id: \.self) { split in
                            Text(split.displayName).tag(split)
                        }
                    }
                    
                    DatePicker("Scheduled Date", selection: $scheduledDate, displayedComponents: [.date, .hourAndMinute])
                }
                
                Section("Mesocycle") {
                    if mesocycleService.mesocycles.isEmpty {
                        Text("No active mesocycles")
                            .foregroundColor(.secondary)
                    } else {
                        Picker("Select Mesocycle", selection: $selectedMesocycle) {
                            Text("None").tag(nil as Mesocycle?)
                            ForEach(mesocycleService.mesocycles) { mesocycle in
                                Text(mesocycle.name).tag(mesocycle as Mesocycle?)
                            }
                        }
                    }
                }
                
                Section("Description") {
                    TextEditor(text: $description)
                        .frame(height: 100)
                }
                
                Section("Notes") {
                    TextEditor(text: $notes)
                        .frame(height: 80)
                }
            }
            .navigationTitle("New Workout")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") {
                        dismiss()
                    }
                }
                
                ToolbarItem(placement: .confirmationAction) {
                    Button("Create") {
                        Task {
                            await createWorkout()
                        }
                    }
                    .disabled(name.isEmpty || selectedMesocycle == nil)
                }
            }
            .task {
                await mesocycleService.fetchMesocycles()
                selectedMesocycle = mesocycleService.mesocycles.first { $0.status == .active }
            }
        }
    }
    
    private func createWorkout() async {
        guard let mesocycle = selectedMesocycle else { return }
        
        let workout = WorkoutCreate(
            mesocycleId: mesocycle.id,
            microcycleId: nil,
            name: name,
            description: description.isEmpty ? nil : description,
            scheduledDate: scheduledDate,
            split: selectedSplit,
            notes: notes.isEmpty ? nil : notes
        )
        
        let success = await workoutService.createWorkout(workout)
        if success {
            dismiss()
        }
    }
}

#Preview {
    CreateWorkoutView(workoutService: WorkoutService())
}
