export interface AnalysisModel {
  Coverage: number[];
  Conflicts: string[];
  Polarity: string[];
  Overlaps: string[];
  Correct?: number[];
  Incorrect?: number[];
  EmpAcc?: string[];
  index: string[];
}
