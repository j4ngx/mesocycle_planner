//
//  WorkoutService.swift
//  MesocyclePlanner
//

import Foundation

class WorkoutService: ObservableObject {
    @Published var workouts: [Workout] = []
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    private let apiClient = APIClient.shared
    
    func fetchWorkouts(mesocycleId: UUID? = nil, completed: Bool? = nil) async {
        await MainActor.run { isLoading = true }
        
        var queryParams = [String: String]()
        if let mesocycleId = mesocycleId {
            queryParams["mesocycle_id"] = mesocycleId.uuidString
        }
        if let completed = completed {
            queryParams["completed"] = String(completed)
        }
        
        let queryString = queryParams.isEmpty ? "" : "?" + queryParams.map { "\($0.key)=\($0.value)" }.joined(separator: "&")
        
        do {
            let response: WorkoutListResponse = try await apiClient.request(endpoint: "/workouts\(queryString)")
            await MainActor.run {
                self.workouts = response.workouts
                self.isLoading = false
            }
        } catch {
            await MainActor.run {
                self.errorMessage = error.localizedDescription
                self.isLoading = false
            }
        }
    }
    
    func getWorkout(id: UUID) async -> Workout? {
        do {
            let workout: Workout = try await apiClient.request(endpoint: "/workouts/\(id.uuidString)")
            return workout
        } catch {
            await MainActor.run {
                self.errorMessage = error.localizedDescription
            }
            return nil
        }
    }
    
    func createWorkout(_ workout: WorkoutCreate) async -> Bool {
        await MainActor.run { isLoading = true }
        
        do {
            let created: Workout = try await apiClient.request(
                endpoint: "/workouts",
                method: .post,
                body: workout
            )
            await MainActor.run {
                self.workouts.append(created)
                self.isLoading = false
            }
            return true
        } catch {
            await MainActor.run {
                self.errorMessage = error.localizedDescription
                self.isLoading = false
            }
            return false
        }
    }
    
    func completeWorkout(id: UUID, durationMinutes: Int?, notes: String?) async -> Bool {
        await MainActor.run { isLoading = true }
        
        let request = CompleteWorkoutRequest(durationMinutes: durationMinutes, notes: notes)
        
        do {
            let updated: Workout = try await apiClient.request(
                endpoint: "/workouts/\(id.uuidString)/complete",
                method: .post,
                body: request
            )
            await MainActor.run {
                if let index = self.workouts.firstIndex(where: { $0.id == id }) {
                    self.workouts[index] = updated
                }
                self.isLoading = false
            }
            return true
        } catch {
            await MainActor.run {
                self.errorMessage = error.localizedDescription
                self.isLoading = false
            }
            return false
        }
    }
    
    func deleteWorkout(id: UUID) async -> Bool {
        do {
            try await apiClient.request(
                endpoint: "/workouts/\(id.uuidString)",
                method: .delete
            )
            await MainActor.run {
                self.workouts.removeAll { $0.id == id }
            }
            return true
        } catch {
            await MainActor.run {
                self.errorMessage = error.localizedDescription
            }
            return false
        }
    }
}

// MARK: - Response Models
struct WorkoutListResponse: Codable {
    let workouts: [Workout]
    let totalCount: Int
    let page: Int
    let totalPages: Int
}

struct CompleteWorkoutRequest: Codable {
    let durationMinutes: Int?
    let notes: String?
}
