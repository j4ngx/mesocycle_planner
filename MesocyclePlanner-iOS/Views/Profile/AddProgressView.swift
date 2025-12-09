//
//  AddProgressView.swift
//  MesocyclePlanner
//

import SwiftUI

struct AddProgressView: View {
    @ObservedObject var progressService: ProgressService
    @Environment(\.dismiss) var dismiss
    
    let selectedMetric: MetricType
    
    @State private var date = Date()
    @State private var value: String = ""
    @State private var notes: String = ""
    @State private var unit: String
    
    init(progressService: ProgressService, selectedMetric: MetricType) {
        self.progressService = progressService
        self.selectedMetric = selectedMetric
        _unit = State(initialValue: selectedMetric.defaultUnit)
    }
    
    var body: some View {
        NavigationStack {
            Form {
                Section("Measurement Details") {
                    Picker("Type", selection: .constant(selectedMetric)) {
                        Text(selectedMetric.displayName).tag(selectedMetric)
                    }
                    .disabled(true)
                    
                    DatePicker("Date", selection: $date, displayedComponents: .date)
                    
                    HStack {
                        TextField("Value", text: $value)
                            .keyboardType(.decimalPad)
                        
                        Text(unit)
                            .foregroundColor(.secondary)
                    }
                }
                
                Section("Notes") {
                    TextEditor(text: $notes)
                        .frame(height: 100)
                }
            }
            .navigationTitle("Add Progress")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") {
                        dismiss()
                    }
                }
                
                ToolbarItem(placement: .confirmationAction) {
                    Button("Save") {
                        Task {
                            await saveProgress()
                        }
                    }
                    .disabled(value.isEmpty)
                }
            }
        }
    }
    
    private func saveProgress() async {
        guard let valueDouble = Double(value) else { return }
        
        let progress = ProgressCreate(
            date: date,
            metricType: selectedMetric,
            value: valueDouble,
            unit: unit,
            notes: notes.isEmpty ? nil : notes
        )
        
        let success = await progressService.createProgress(progress)
        if success {
            dismiss()
        }
    }
}
