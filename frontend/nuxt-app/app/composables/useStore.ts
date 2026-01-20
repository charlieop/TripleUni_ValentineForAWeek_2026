export const useStore = () => {
  const setToken = (token: string): void => {
    localStorage.setItem("token", token);
  };
  const getToken = (): string | null => {
    return localStorage.getItem("token");
  };
  const clearToken = (): void => {
    localStorage.removeItem("token");
  };

  const setApplicantId = (applicationId: string): void => {
    if (
      !/^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$/.test(
        applicationId
      )
    ) {
      throw new Error("Invalid UUID format");
    }
    localStorage.setItem("applicantId", applicationId);
  };
  const getApplicantId = (): string | null => {
    return localStorage.getItem("applicantId");
  };
  const clearApplicantId = (): void => {
    localStorage.removeItem("applicantId");
  };

  const setApplicationFormData = (data: any): void => {
    localStorage.setItem("applicationFormData", JSON.stringify(data));
  };

  const getApplicationFormData = (): any | null => {
    const data = localStorage.getItem("applicationFormData");
    return data ? JSON.parse(data) : null;
  };

  const deleteApplicationFormData = (): void => {
    localStorage.removeItem("applicationFormData");
  };

  return {
    setToken,
    getToken,
    clearToken,

    setApplicantId,
    getApplicantId,
    clearApplicantId,

    setApplicationFormData,
    getApplicationFormData,
    deleteApplicationFormData,
  };
};
