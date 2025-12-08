//
//  MesocycleService.swift
//  MesocyclePlanner
//

import Foundation

class MesocycleService: ObservableObject {
    @Published var mesocycles: [Mesocycle] = []
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    private let apiClient = APIClient.shared
    
    func fetchMesocycles() async {
        await MainActor.run { isLoading = true }
        
        do {
            let fetchedMesocycles: [Mesocycle] = try await apiClient.request(endpoint: "/mesocycles")
            await MainActor.run {
                self.mesocycles = fetchedMesocycles
                self.isLoading = false
            }
        } catch {
            await MainActor.run {
                self.errorMessage = error.localizedDescription
                self.isLoading = false
            }
        }
    }
    
    func createMesocycle(_ mesocycle: MesocycleCreate) async -> Bool {
        await MainActor.run { isLoading = true }
        
        do {
            let created: Mesocycle = try await apiClient.request(
                endpoint: "/mesocycles",
                method: .post,
                body: mesocycle
            )
            await MainActor.run {
                self.mesocycles.append(created)
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
}
