export interface AnalysisModel {
  Coverage: number[];
  Conflicts: number[];
  Polarity: number[];
  Overlaps: number[];
  Correct?: number[];
  Incorrect?: number[];
  EmpAcc?: string[];
  index: string[];
}
