//
//  ExerciseService.swift
//  MesocyclePlanner
//

import Foundation

class ExerciseService: ObservableObject {
    @Published var exercises: [Exercise] = []
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    private let apiClient = APIClient.shared
    
    func fetchExercises(muscleGroup: MuscleGroup? = nil, type: ExerciseType? = nil) async {
        await MainActor.run { isLoading = true }
        
        var endpoint = "/exercises?"
        if let group = muscleGroup {
            endpoint += "muscle_group=\(group.rawValue)&"
        }
        if let exerciseType = type {
            endpoint += "type=\(exerciseType.rawValue)&"
        }
        
        do {
            let fetchedExercises: [Exercise] = try await apiClient.request(endpoint: endpoint)
            await MainActor.run {
                self.exercises = fetchedExercises
                self.isLoading = false
            }
        } catch {
            await MainActor.run {
                self.errorMessage = error.localizedDescription
                self.isLoading = false
            }
        }
    }
    
    func searchExercises(query: String) async {
        await MainActor.run { isLoading = true }
        
        do {
            let results: [Exercise] = try await apiClient.request(endpoint: "/exercises/search?q=\(query)")
            await MainActor.run {
                self.exercises = results
                self.isLoading = false
            }
        } catch {
            await MainActor.run {
                self.errorMessage = error.localizedDescription
                self.isLoading = false
            }
        }
    }
}
