//
//  MesocycleListView.swift
//  MesocyclePlanner
//

import SwiftUI

struct MesocycleListView: View {
    @StateObject private var mesocycleService = MesocycleService()
    @State private var showCreateSheet = false
    
    var body: some View {
        NavigationStack {
            Group {
                if mesocycleService.isLoading {
                    ProgressView()
                } else if mesocycleService.mesocycles.isEmpty {
                    ContentUnavailableView(
                        "No Mesocycles",
                        systemImage: "calendar",
                        description: Text("Create your first training mesocycle")
                    )
                } else {
                    List(mesocycleService.mesocycles) { mesocycle in
                        NavigationLink(destination: MesocycleDetailView(mesocycle: mesocycle)) {
                            MesocycleCard(mesocycle: mesocycle)
                        }
                        .listRowInsets(EdgeInsets())
                        .listRowSeparator(.hidden)
                        .padding(.horizontal)
                        .padding(.vertical, AppSpacing.xs)
                    }
                    .listStyle(.plain)
                }
            }
            .navigationTitle("Mesocycles")
            .toolbar {
                ToolbarItem(placement: .primaryAction) {
                    Button {
                        showCreateSheet = true
                    } label: {
                        Image(systemName: "plus.circle.fill")
                            .font(.title2)
                    }
                }
            }
            .sheet(isPresented: $showCreateSheet) {
                CreateMesocycleView(mesocycleService: mesocycleService)
            }
            .task {
                await mesocycleService.fetchMesocycles()
            }
        }
    }
}

struct MesocycleCard: View {
    let mesocycle: Mesocycle
    
    var body: some View {
        VStack(alignment: .leading, spacing: AppSpacing.md) {
            // Header
            HStack {
                VStack(alignment: .leading, spacing: 4) {
                    Text(mesocycle.name)
                        .font(AppTypography.headline)
                        .fontWeight(.bold)
                    
                    Text(mesocycle.periodizationModel.displayName)
                        .font(AppTypography.caption)
                        .foregroundColor(.secondary)
                }
                
                Spacer()
                
                StatusBadge(status: mesocycle.status)
            }
            
            // Info grid
            HStack(spacing: AppSpacing.lg) {
                InfoItem(icon: mesocycle.goal.icon, text: mesocycle.goal.displayName)
                InfoItem(icon: "calendar", text: "\(mesocycle.durationWeeks) weeks")
                InfoItem(icon: "figure.run", text: "\(mesocycle.weeklyFrequency)x/week")
            }
            
            // Progress bar
            if mesocycle.status == .active {
                ProgressView(value: 0.3)
                    .tint(AppColors.primary)
            }
        }
        .padding()
        .background(AppColors.cardBackground)
        .cornerRadius(AppCornerRadius.md)
        .shadow(color: .black.opacity(0.05), radius: 5, x: 0, y: 2)
    }
}

struct StatusBadge: View {
    let status: MesocycleStatus
    
    var body: some View {
        Text(status.displayName)
            .font(AppTypography.caption)
            .fontWeight(.semibold)
            .padding(.horizontal, AppSpacing.sm)
            .padding(.vertical, 4)
            .background(Color(status.color).opacity(0.2))
            .foregroundColor(Color(status.color))
            .cornerRadius(AppCornerRadius.sm)
    }
}

struct InfoItem: View {
    let icon: String
    let text: String
    
    var body: some View {
        HStack(spacing: 4) {
            Image(systemName: icon)
                .font(.caption)
            Text(text)
                .font(AppTypography.caption)
        }
        .foregroundColor(.secondary)
    }
}

struct CreateMesocycleView: View {
    @Environment(\.dismiss) var dismiss
    @ObservedObject var mesocycleService: MesocycleService
    
    @State private var name = ""
    @State private var description = ""
    @State private var selectedModel: PeriodizationModel = .linear
    @State private var selectedGoal: TrainingGoal = .hypertrophy
    @State private var durationWeeks = 12
    @State private var weeklyFrequency = 4
    @State private var startDate = Date()
    
    var endDate: Date {
        Calendar.current.date(byAdding: .weekOfYear, value: durationWeeks, to: startDate) ?? startDate
    }
    
    var body: some View {
        NavigationStack {
            Form {
                Section("Basic Information") {
                    TextField("Mesocycle Name", text: $name)
                    TextField("Description (Optional)", text: $description, axis: .vertical)
                        .lineLimit(3...6)
                }
                
                Section("Training Configuration") {
                    Picker("Periodization Model", selection: $selectedModel) {
                        ForEach(PeriodizationModel.allCases, id: \.self) { model in
                            Text(model.displayName).tag(model)
                        }
                    }
                    
                    Picker("Training Goal", selection: $selectedGoal) {
                        ForEach(TrainingGoal.allCases, id: \.self) { goal in
                            HStack {
                                Image(systemName: goal.icon)
                                Text(goal.displayName)
                            }
                            .tag(goal)
                        }
                    }
                }
                
                Section("Schedule") {
                    DatePicker("Start Date", selection: $startDate, displayedComponents: .date)
                    
                    Stepper("Duration: \(durationWeeks) weeks", value: $durationWeeks, in: 4...16)
                    
                    Stepper("Frequency: \(weeklyFrequency)x/week", value: $weeklyFrequency, in: 3...6)
                    
                    HStack {
                        Text("End Date")
                        Spacer()
                        Text(endDate, style: .date)
                            .foregroundColor(.secondary)
                    }
                }
                
                Section {
                    PrimaryButton(
                        title: "Create Mesocycle",
                        isLoading: mesocycleService.isLoading
                    ) {
                        Task {
                            let mesocycle = MesocycleCreate(
                                name: name,
                                description: description.isEmpty ? nil : description,
                                periodizationModel: selectedModel,
                                goal: selectedGoal,
                                durationWeeks: durationWeeks,
                                startDate: startDate,
                                endDate: endDate,
                                trainingLevel: "intermediate",
                                weeklyFrequency: weeklyFrequency
                            )
                            
                            let success = await mesocycleService.createMesocycle(mesocycle)
                            if success {
                                dismiss()
                            }
                        }
                    }
                    .disabled(name.isEmpty)
                }
            }
            .navigationTitle("New Mesocycle")
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
