//
//  WorkoutListView.swift
//  MesocyclePlanner
//

import SwiftUI

struct WorkoutListView: View {
    @StateObject private var workoutService = WorkoutService()
    @State private var selectedFilter: WorkoutFilter = .upcoming
    @State private var showCreateSheet = false
    
    enum WorkoutFilter: String, CaseIterable {
        case upcoming = "Upcoming"
        case completed = "Completed"
        case all = "All"
    }
    
    var filteredWorkouts: [Workout] {
        switch selectedFilter {
        case .upcoming:
            return workoutService.workouts.filter { !$0.completed && $0.scheduledDate >= Date() }
        case .completed:
            return workoutService.workouts.filter { $0.completed }
        case .all:
            return workoutService.workouts
        }
    }
    
    var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
                // Filter picker
                Picker("Filter", selection: $selectedFilter) {
                    ForEach(WorkoutFilter.allCases, id: \.self) { filter in
                        Text(filter.rawValue).tag(filter)
                    }
                }
                .pickerStyle(.segmented)
                .padding()
                
                if workoutService.isLoading {
                    ProgressView()
                        .frame(maxHeight: .infinity)
                } else if filteredWorkouts.isEmpty {
                    ContentUnavailableView(
                        "No Workouts",
                        systemImage: "dumbbell.fill",
                        description: Text(emptyStateMessage)
                    )
                } else {
                    List {
                        ForEach(filteredWorkouts) { workout in
                            NavigationLink(destination: WorkoutDetailView(workout: workout)) {
                                WorkoutRow(workout: workout)
                            }
                            .listRowInsets(EdgeInsets())
                            .listRowSeparator(.hidden)
                            .padding(.horizontal)
                            .padding(.vertical, AppSpacing.xs)
                        }
                    }
                    .listStyle(.plain)
                }
            }
            .navigationTitle("Workouts")
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
                CreateWorkoutView(workoutService: workoutService)
            }
            .task {
                await workoutService.fetchWorkouts()
            }
            .onChange(of: selectedFilter) { _ in
                // Could refetch with filter if backend supports it
            }
        }
    }
    
    var emptyStateMessage: String {
        switch selectedFilter {
        case .upcoming:
            return "No upcoming workouts scheduled"
        case .completed:
            return "No completed workouts yet"
        case .all:
            return "Create your first workout"
        }
    }
}

struct WorkoutRow: View {
    let workout: Workout
    
    var isOverdue: Bool {
        !workout.completed && workout.scheduledDate < Date()
    }
    
    var body: some View {
        HStack(spacing: AppSpacing.md) {
            // Status indicator
            Circle()
                .fill(statusColor)
                .frame(width: 12, height: 12)
            
            VStack(alignment: .leading, spacing: 4) {
                Text(workout.name)
                    .font(AppTypography.headline)
                    .fontWeight(.medium)
                
                HStack(spacing: AppSpacing.xs) {
                    Image(systemName: "calendar")
                        .font(.caption)
                    Text(workout.scheduledDate, style: .date)
                        .font(AppTypography.caption)
                    
                    if let split = workout.split {
                        Text("•")
                            .font(.caption)
                        Text(split.displayName)
                            .font(AppTypography.caption)
                    }
                }
                .foregroundColor(.secondary)
            }
            
            Spacer()
            
            if workout.completed {
                Image(systemName: "checkmark.circle.fill")
                    .foregroundColor(.green)
                    .font(.title3)
            } else if isOverdue {
                Image(systemName: "exclamationmark.circle.fill")
                    .foregroundColor(.orange)
                    .font(.title3)
            } else {
                Image(systemName: "chevron.right")
                    .foregroundColor(.secondary)
                    .font(.caption)
            }
        }
        .padding()
        .background(AppColors.cardBackground)
        .cornerRadius(AppCornerRadius.md)
    }
    
    var statusColor: Color {
        if workout.completed {
            return .green
        } else if isOverdue {
            return .orange
        } else {
            return AppColors.primary
        }
    }
}

#Preview {
    WorkoutListView()
}
