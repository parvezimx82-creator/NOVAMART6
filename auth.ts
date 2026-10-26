export const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

async function csrfToken(): Promise<string> {
  const response = await fetch(`${API}/auth/csrf/`, { credentials: "include" });
  const data = await response.json().catch(() => ({}));
  return data.csrfToken || "";
}
export async function apiPost(path: string, data: unknown) {
  const csrf = await csrfToken();
  const response = await fetch(`${API}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRFToken": csrf },
    credentials: "include",
    body: JSON.stringify(data),
  });
  const result = await response.json().catch(() => ({}));
  if (!response.ok) {
    const detail = result.detail || result.email?.[0] || result.username?.[0] || result.password?.[0] || result.password_confirm?.[0] || "অনুরোধটি সম্পন্ন হয়নি।";
    throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
  }
  return result;
}
