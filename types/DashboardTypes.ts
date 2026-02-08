export type DashboardStatType = {
  id: string;
  title: string;
  value: string;
  icon: React.ReactNode;
  bgColor: string;
  textColor: string;
  bottomValue: string;
  description: string;
};

export interface ProjectType {
  id: string;
  name: string;
  deadline: string;
  progress: number;
  status: string;
  assignedAvatars: string[];
  plays?: number;
}

export interface TeamsProps {
  name: string;
  role: string;
  avatar: string;
  tasksAssigned: number;
}

export interface ActivityLogType {
  description: string;
  timestamp: string;

  colorClass: string;
}

export type Task = {
  id: string;
  title: string;
  priority: "Low" | "Medium" | "High" | "Critical";
  badgeVariant: "primary" | "warning" | "info" | "danger";
};

export interface EventType {
  title: string;
  date: string;
  time: string;
  platform: string;
}

export interface PopularQuizType {
  title: string;
  attempts: number;
  avg_score: number;
}

export interface AdminStatsType {
  total_users: number;
  total_quizzes: number;
  total_categories: number;
  popular_quizzes: PopularQuizType[];
  success_rates: {
    [key: string]: {
      avg_score: number;
      success_rate: number;
    }
  };
}
