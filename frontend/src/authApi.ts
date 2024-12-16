import axiosInstance from "./axiosInstance";

function handleErrorResponse(error: any, defaultMessage: string): never {
    if (error.response) {
      const status = error.response.status;
  
      const errorMessages: Record<number, string> = {
        404: "User not found.",
        401: "Invalid credentials.",
        409: "User already exists.",
      };
  
      const message = errorMessages[status] || defaultMessage;
      throw new Error(message);
    }
  
    throw new Error(defaultMessage);
  }
  
  export async function handleLogin(
    email: string,
    password: string
  ): Promise<void> {
    try {
      const response = await axiosInstance.post("/login", {
        email,
        password,
      });
  
      if (response.status !== 200) {
        throw new Error("Error during login.");
      }
    } catch (error) {
      handleErrorResponse(error, "Failed to log in. Please try again.");
    }
  }
  
  export async function registerUser(
    username: string,
    email: string,
    password: string
  ): Promise<void> {
    try {
      const response = await axiosInstance.post("/register", {
        username,
        email,
        password,
      });
  
      if (response.status !== 200) {
        throw new Error("Error during registration.");
      }
    } catch (error) {
      handleErrorResponse(error, "Failed to register. Please try again.");
    }
  }
  