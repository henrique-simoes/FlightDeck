import { fallbackAssignment } from "./fallback";
import type { AssignmentResponse, PersonaId } from "./types";

const API_BASE_URL = import.meta.env.VITE_FLIGHTDECK_API_BASE_URL ?? "http://localhost:8000";

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "content-type": "application/json",
      ...(init?.headers ?? {}),
    },
  });
  if (!response.ok) {
    throw new Error(`FlightDeck API ${response.status}: ${path}`);
  }
  return response.json() as Promise<T>;
}

export async function loadAssignment(persona: PersonaId): Promise<AssignmentResponse> {
  try {
    const experiment = await apiFetch<{ id: string }>("/experiments/default");
    return await apiFetch<AssignmentResponse>(
      `/experiments/${experiment.id}/assignment?persona=${persona}`,
    );
  } catch (error) {
    console.warn(error);
    return fallbackAssignment(persona);
  }
}

export function postTelemetry(
  eventPath: "ui-rendered" | "first-action" | "task-completed" | "feedback",
  payload: Record<string, unknown>,
) {
  return apiFetch(`/events/${eventPath}`, {
    method: "POST",
    body: JSON.stringify(payload),
  }).catch((error) => {
    console.warn(error);
  });
}
