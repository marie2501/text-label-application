export interface WorkflowModel {
  id?: number;
  title: string;
  is_public: boolean;
  creation_date?: string;
  contributors?: string[];
  creator?: string;

}
