export interface WorkflowModel {
  id?: number;
  title: string;
  is_public: boolean;
  creation_date?: string;
  contributors?: string[];
  creator?: string;
  splitting_ratio_labeled_test?: number;

}
