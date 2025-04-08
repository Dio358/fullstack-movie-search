import { BASE_URL } from "./backendURL";

export const logIn = async (userName: string, password: string) => {
  try {
    const res = await fetch(`${BASE_URL}/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username: userName, password: password }),
    });

    const data = await res.json();

    if (res.ok) {
      return data;
    } else {
      return null;
    }
  } catch (err) {
    console.error("Failed to fetch from backend:", err);
  }
};


export const createAccount = async (userName: string, password: string) => {
    try {
      const res = await fetch(`${BASE_URL}/createUser`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username: userName, password: password }),
      });
  
      const data = await res.json();
  
      if (res.ok) {
        return { success: true };
      } else if (res.status === 409) {
        return { success: false, message: "UserName exists already" };
      } else {
        console.log("Response:", data, res.status);
        return { success: false, message: "An unexpected error occurred" };
      }
    } catch (err) {
      console.error("Failed to fetch from backend:", err);
      return { success: false, message: "Failed to connect to backend." };
    }
  };
  