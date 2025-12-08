//
//  ExerciseLibraryView.swift
//  MesocyclePlanner
//

import SwiftUI

struct ExerciseLibraryView: View {
    @StateObject private var exerciseService = ExerciseService()
    @State private var searchText = ""
    @State private var selectedMuscleGroup: MuscleGroup?
    @State private var showFilters = false
    
    var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
                // Filter chips
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: AppSpacing.sm) {
                        FilterChip(
                            title: "All",
                            isSelected: selectedMuscleGroup == nil
                        ) {
                            selectedMuscleGroup = nil
                            Task {
                                await exerciseService.fetchExercises()
                            }
                        }
                        
                        ForEach(MuscleGroup.allCases, id: \.self) { group in
                            FilterChip(
                                title: group.displayName,
                                isSelected: selectedMuscleGroup == group
                            ) {
                                selectedMuscleGroup = group
                                Task {
                                    await exerciseService.fetchExercises(muscleGroup: group)
                                }
                            }
                        }
                    }
                    .padding(.horizontal)
                }
                .padding(.vertical, AppSpacing.sm)
                .background(AppColors.secondaryBackground)
                
                // Exercise list
                if exerciseService.isLoading {
                    ProgressView()
                        .frame(maxWidth: .infinity, maxHeight: .infinity)
                } else if exerciseService.exercises.isEmpty {
                    ContentUnavailableView(
                        "No Exercises",
                        systemImage: "dumbbell",
                        description: Text("No exercises found")
                    )
                } else {
                    List(exerciseService.exercises) { exercise in
                        NavigationLink(destination: ExerciseDetailView(exercise: exercise)) {
                            ExerciseRow(exercise: exercise)
                        }
                    }
                    .listStyle(.plain)
                }
            }
            .navigationTitle("Exercises")
            .searchable(text: $searchText, prompt: "Search exercises")
            .onChange(of: searchText) { _, newValue in
                if !newValue.isEmpty {
                    Task {
                        await exerciseService.searchExercises(query: newValue)
                    }
                } else {
                    Task {
                        await exerciseService.fetchExercises(muscleGroup: selectedMuscleGroup)
                    }
                }
            }
            .task {
                await exerciseService.fetchExercises()
            }
        }
    }
}

struct ExerciseRow: View {
    let exercise: Exercise
    
    var body: some View {
        HStack(spacing: AppSpacing.md) {
            // Icon
            Image(systemName: exercise.muscleGroup.icon)
                .font(.title2)
                .foregroundStyle(AppColors.primary)
                .frame(width: 40, height: 40)
                .background(AppColors.primary.opacity(0.1))
                .cornerRadius(AppCornerRadius.sm)
            
            VStack(alignment: .leading, spacing: 4) {
                Text(exercise.name)
                    .font(AppTypography.headline)
                
                HStack {
                    Text(exercise.muscleGroup.displayName)
                        .font(AppTypography.caption)
                        .foregroundColor(.secondary)
                    
                    Text("•")
                        .foregroundColor(.secondary)
                    
                    Text(exercise.type.displayName)
                        .font(AppTypography.caption)
                        .foregroundColor(.secondary)
                }
            }
            
            Spacer()
            
            Image(systemName: "chevron.right")
                .font(.caption)
                .foregroundColor(.secondary)
        }
        .padding(.vertical, AppSpacing.xs)
    }
}

struct FilterChip: View {
    let title: String
    let isSelected: Bool
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            Text(title)
                .font(AppTypography.callout)
                .fontWeight(isSelected ? .semibold : .regular)
                .padding(.horizontal, AppSpacing.md)
                .padding(.vertical, AppSpacing.sm)
                .background(isSelected ? AppColors.primary : AppColors.cardBackground)
                .foregroundColor(isSelected ? .white : .primary)
                .cornerRadius(AppCornerRadius.lg)
        }
    }
}

struct ExerciseDetailView: View {
    let exercise: Exercise
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: AppSpacing.lg) {
                // Header
                VStack(alignment: .leading, spacing: AppSpacing.sm) {
                    HStack {
                        Image(systemName: exercise.muscleGroup.icon)
                            .font(.largeTitle)
                            .foregroundStyle(AppColors.primary)
                        
                        Spacer()
                        
                        VStack(alignment: .trailing) {
                            Text(exercise.muscleGroup.displayName)
                                .font(AppTypography.caption)
                                .foregroundColor(.secondary)
                            Text(exercise.type.displayName)
                                .font(AppTypography.caption)
                                .foregroundColor(.secondary)
                        }
                    }
                    
                    Text(exercise.name)
                        .font(AppTypography.title)
                        .fontWeight(.bold)
                }
                .padding()
                .background(AppColors.cardBackground)
                .cornerRadius(AppCornerRadius.md)
                
                // Execution
                if let execution = exercise.execution {
                    InfoSection(title: "Execution", icon: "text.alignleft") {
                        Text(execution)
                            .font(AppTypography.body)
                    }
                }
                
                // Muscles
                InfoSection(title: "Primary Muscles", icon: "figure.strengthtraining.traditional") {
                    FlowLayout(items: exercise.primaryMuscles) { muscle in
                        MuscleTag(muscle: muscle, isPrimary: true)
                    }
                }
                
                if let secondary = exercise.secondaryMuscles, !secondary.isEmpty {
                    InfoSection(title: "Secondary Muscles", icon: "figure.walk") {
                        FlowLayout(items: secondary) { muscle in
                            MuscleTag(muscle: muscle, isPrimary: false)
                        }
                    }
                }
                
                // Common mistakes
                if let mistakes = exercise.commonMistakes, !mistakes.isEmpty {
                    InfoSection(title: "Common Mistakes", icon: "exclamationmark.triangle") {
                        VStack(alignment: .leading, spacing: AppSpacing.sm) {
                            ForEach(mistakes, id: \.self) { mistake in
                                HStack(alignment: .top, spacing: AppSpacing.sm) {
                                    Text("•")
                                    Text(mistake)
                                        .font(AppTypography.body)
                                }
                            }
                        }
                    }
                }
            }
            .padding()
        }
        .navigationBarTitleDisplayMode(.inline)
        .background(AppColors.secondaryBackground)
    }
}

struct InfoSection<Content: View>: View {
    let title: String
    let icon: String
    @ViewBuilder let content: Content
    
    var body: some View {
        VStack(alignment: .leading, spacing: AppSpacing.md) {
            HStack {
                Image(systemName: icon)
                    .foregroundStyle(AppColors.primary)
                Text(title)
                    .font(AppTypography.headline)
            }
            
            content
        }
        .padding()
        .background(AppColors.cardBackground)
        .cornerRadius(AppCornerRadius.md)
    }
}

struct MuscleTag: View {
    let muscle: String
    let isPrimary: Bool
    
    var body: some View {
        Text(muscle.replacingOccurrences(of: "_", with: " ").capitalized)
            .font(AppTypography.caption)
            .padding(.horizontal, AppSpacing.sm)
            .padding(.vertical, 4)
            .background(isPrimary ? AppColors.primary.opacity(0.2) : AppColors.secondary.opacity(0.2))
            .foregroundColor(isPrimary ? AppColors.primary : AppColors.secondary)
            .cornerRadius(AppCornerRadius.sm)
    }
}

struct FlowLayout<Item, ItemView: View>: View {
    let items: [Item]
    let itemView: (Item) -> ItemView
    
    @State private var totalHeight = CGFloat.zero
    
    var body: some View {
        VStack {
            GeometryReader { geometry in
                self.generateContent(in: geometry)
            }
        }
        .frame(height: totalHeight)
    }
    
    private func generateContent(in g: GeometryProxy) -> some View {
        var width = CGFloat.zero
        var height = CGFloat.zero
        
        return ZStack(alignment: .topLeading) {
            ForEach(Array(items.enumerated()), id: \.offset) { index, item in
                itemView(item)
                    .padding([.horizontal, .vertical], 4)
                    .alignmentGuide(.leading, computeValue: { d in
                        if (abs(width - d.width) > g.size.width) {
                            width = 0
                            height -= d.height
                        }
                        let result = width
                        if index == items.count - 1 {
                            width = 0
                        } else {
                            width -= d.width
                        }
                        return result
                    })
                    .alignmentGuide(.top, computeValue: { d in
                        let result = height
                        if index == items.count - 1 {
                            height = 0
                        }
                        return result
                    })
            }
        }
        .background(viewHeightReader($totalHeight))
    }
    
    private func viewHeightReader(_ binding: Binding<CGFloat>) -> some View {
        return GeometryReader { geometry -> Color in
            let rect = geometry.frame(in: .local)
            DispatchQueue.main.async {
                binding.wrappedValue = rect.size.height
            }
            return .clear
        }
    }
}
