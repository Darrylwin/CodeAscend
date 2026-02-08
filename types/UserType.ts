export interface UserType {
    id: string;
    name: string;
    email: string;
    role: "user" | "admin";
    created_at: string;
    updated_at: string | null;
}
