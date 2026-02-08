export interface CategoryType {
  id: string;
  name: string;
  description: string;
  // quizCount: number; // Removed as API does not return this
  is_active: boolean;
  status?: string; // Optional for compatibility if needed, but prefer is_active
  icon_url: string;
  created_at: string;
  updated_at: string | null;
}
