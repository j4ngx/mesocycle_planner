//
//  ProgressService.swift
//  MesocyclePlanner
//

import Foundation

class ProgressService: ObservableObject {
    @Published var progressEntries: [Progress] = []
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    private let apiClient = APIClient.shared
    
    func fetchProgress(metricType: MetricType? = nil, startDate: Date? = nil, endDate: Date? = nil) async {
        await MainActor.run { isLoading = true }
        
        var queryParams = [String: String]()
        if let metricType = metricType {
            queryParams["metric_type"] = metricType.rawValue
        }
        if let startDate = startDate {
            queryParams["start_date"] = ISO8601DateFormatter().string(from: startDate)
        }
        if let endDate = endDate {
            queryParams["end_date"] = ISO8601DateFormatter().string(from: endDate)
        }
        
        let queryString = queryParams.isEmpty ? "" : "?" + queryParams.map { "\($0.key)=\($0.value)" }.joined(separator: "&")
        
        do {
            let response: ProgressListResponse = try await apiClient.request(endpoint: "/progress\(queryString)")
            await MainActor.run {
                self.progressEntries = response.progress
                self.isLoading = false
            }
        } catch {
            await MainActor.run {
                self.errorMessage = error.localizedDescription
                self.isLoading = false
            }
        }
    }
    
    func createProgress(_ progress: ProgressCreate) async -> Bool {
        await MainActor.run { isLoading = true }
        
        do {
            let created: Progress = try await apiClient.request(
                endpoint: "/progress",
                method: .post,
                body: progress
            )
            await MainActor.run {
                self.progressEntries.insert(created, at: 0)
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
    
    func deleteProgress(id: UUID) async -> Bool {
        do {
            try await apiClient.request(
                endpoint: "/progress/\(id.uuidString)",
                method: .delete
            )
            await MainActor.run {
                self.progressEntries.removeAll { $0.id == id }
            }
            return true
        } catch {
            await MainActor.run {
                self.errorMessage = error.localizedDescription
            }
            return false
        }
    }
    
    func updateProgress(id: UUID, _ progress: ProgressCreate) async -> Bool {
        await MainActor.run { isLoading = true }
        
        do {
            let updated: Progress = try await apiClient.request(
                endpoint: "/progress/\(id.uuidString)",
                method: .put,
                body: progress
            )
            await MainActor.run {
                if let index = self.progressEntries.firstIndex(where: { $0.id == id }) {
                    self.progressEntries[index] = updated
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
}

// MARK: - Response Models
struct ProgressListResponse: Codable {
    let progress: [Progress]
    let totalCount: Int
    let page: Int
    let totalPages: Int
}
