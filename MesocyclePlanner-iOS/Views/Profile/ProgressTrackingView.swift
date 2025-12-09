//
//  ProgressTrackingView.swift
//  MesocyclePlanner
//

import SwiftUI
import Charts

struct ProgressTrackingView: View {
    @StateObject private var progressService = ProgressService()
    @State private var selectedMetric: MetricType = .weight
    @State private var showAddSheet = false
    
    var filteredProgress: [Progress] {
        progressService.progressEntries.filter { $0.metricType == selectedMetric }
    }
    
    var body: some View {
        NavigationStack {
            VStack(spacing: 0) {
                // Metric selector
                Picker("Metric Type", selection: $selectedMetric) {
                    ForEach(MetricType.allCases, id: \.self) { metric in
                        Text(metric.displayName).tag(metric)
                    }
                }
                .pickerStyle(.segmented)
                .padding()
                
                if progressService.isLoading {
                    ProgressView()
                        .frame(maxHeight: .infinity)
                } else if filteredProgress.isEmpty {
                    ContentUnavailableView(
                        "No Progress Data",
                        systemImage: "chart.line.uptrend.xyaxis",
                        description: Text("Start tracking your \(selectedMetric.displayName.lowercased())")
                    )
                } else {
                    ScrollView {
                        VStack(spacing: AppSpacing.lg) {
                            // Chart
                            ProgressChartView(entries: filteredProgress, metricType: selectedMetric)
                                .frame(height: 250)
                                .padding()
                            
                            // Stats cards
                            ProgressStatsView(entries: filteredProgress, metricType: selectedMetric)
                                .padding(.horizontal)
                            
                            // History list
                            VStack(alignment: .leading, spacing: AppSpacing.md) {
                                Text("History")
                                    .font(AppTypography.title3)
                                    .fontWeight(.semibold)
                                    .padding(.horizontal)
                                
                                LazyVStack(spacing: AppSpacing.sm) {
                                    ForEach(filteredProgress) { entry in
                                        ProgressEntryRow(entry: entry)
                                            .padding(.horizontal)
                                    }
                                }
                            }
                        }
                        .padding(.vertical)
                    }
                }
            }
            .navigationTitle("Progress")
            .toolbar {
                ToolbarItem(placement: .primaryAction) {
                    Button {
                        showAddSheet = true
                    } label: {
                        Image(systemName: "plus.circle.fill")
                            .font(.title2)
                    }
                }
            }
            .sheet(isPresented: $showAddSheet) {
                AddProgressView(progressService: progressService, selectedMetric: selectedMetric)
            }
            .task {
                await progressService.fetchProgress()
            }
            .onChange(of: selectedMetric) { _ in
                Task {
                    await progressService.fetchProgress(metricType: selectedMetric)
                }
            }
        }
    }
}

struct ProgressChartView: View {
    let entries: [Progress]
    let metricType: MetricType
    
    var body: some View {
        VStack(alignment: .leading, spacing: AppSpacing.sm) {
            Text("Trend")
                .font(AppTypography.headline)
                .fontWeight(.semibold)
            
            Chart(entries) { entry in
                LineMark(
                    x: .value("Date", entry.date),
                    y: .value("Value", entry.value)
                )
                .foregroundStyle(AppColors.primary)
                
                PointMark(
                    x: .value("Date", entry.date),
                    y: .value("Value", entry.value)
                )
                .foregroundStyle(AppColors.primary)
            }
            .chartYAxisLabel(metricType.defaultUnit)
        }
        .padding()
        .background(AppColors.cardBackground)
        .cornerRadius(AppCornerRadius.md)
    }
}

struct ProgressStatsView: View {
    let entries: [Progress]
    let metricType: MetricType
    
    var currentValue: Double {
        entries.first?.value ?? 0
    }
    
    var change: Double {
        guard entries.count >= 2 else { return 0 }
        return currentValue - (entries.last?.value ?? 0)
    }
    
    var changePercent: Double {
        guard let last = entries.last?.value, last != 0 else { return 0 }
        return (change / last) * 100
    }
    
    var body: some View {
        HStack(spacing: AppSpacing.md) {
            StatBox(
                title: "Current",
                value: String(format: "%.1f", currentValue),
                unit: metricType.defaultUnit
            )
            
            StatBox(
                title: "Change",
                value: String(format: "%+.1f", change),
                unit: metricType.defaultUnit,
                trend: change > 0 ? .up : .down
            )
            
            StatBox(
                title: "Progress",
                value: String(format: "%+.1f%%", changePercent),
                unit: "",
                trend: changePercent > 0 ? .up : .down
            )
        }
    }
}

struct StatBox: View {
    let title: String
    let value: String
    let unit: String
    var trend: Trend? = nil
    
    enum Trend {
        case up, down
    }
    
    var body: some View {
        VStack(spacing: AppSpacing.xs) {
            Text(title)
                .font(AppTypography.caption)
                .foregroundColor(.secondary)
            
            HStack(spacing: 4) {
                Text(value)
                    .font(AppTypography.title2)
                    .fontWeight(.bold)
                
                Text(unit)
                    .font(AppTypography.caption)
                    .foregroundColor(.secondary)
                
                if let trend = trend {
                    Image(systemName: trend == .up ? "arrow.up.right" : "arrow.down.right")
                        .font(.caption)
                        .foregroundColor(trend == .up ? .green : .red)
                }
            }
        }
        .frame(maxWidth: .infinity)
        .padding()
        .background(AppColors.cardBackground)
        .cornerRadius(AppCornerRadius.md)
    }
}

struct ProgressEntryRow: View {
    let entry: Progress
    
    var body: some View {
        HStack {
            VStack(alignment: .leading, spacing: 4) {
                Text(entry.date, style: .date)
                    .font(AppTypography.subheadline)
                    .fontWeight(.medium)
                
                if let notes = entry.notes {
                    Text(notes)
                        .font(AppTypography.caption)
                        .foregroundColor(.secondary)
                }
            }
            
            Spacer()
            
            VStack(alignment: .trailing, spacing: 4) {
                Text("\(entry.value, specifier: "%.1f") \(entry.unit ?? "")")
                    .font(AppTypography.headline)
                    .fontWeight(.semibold)
                
                Text(entry.metricType.displayName)
                    .font(AppTypography.caption)
                    .foregroundColor(.secondary)
            }
        }
        .padding()
        .background(AppColors.cardBackground)
        .cornerRadius(AppCornerRadius.sm)
    }
}

#Preview {
    ProgressTrackingView()
}
