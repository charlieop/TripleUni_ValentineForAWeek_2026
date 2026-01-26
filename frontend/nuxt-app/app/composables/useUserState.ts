const { get } = useRequest();

export enum UserStates {
    UNKNOWN = "UNKNOWN",
    MAINTENANCE = "MAINTENANCE",

    NOT_STARTED = "NOT_STARTED",

    APPLICATION_START = "APPLICATION_START",
    APPLIED = "APPLIED",
    PAID = "PAID",
    APPLICATION_END = "APPLICATION_END",
    QUITTED = "QUITTED",

    WAITING_FOR_FIRST_MATCH_RESULT = "WAITING_FOR_FIRST_MATCH_RESULT",
    FIRST_MATCH_RESULT_RELEASE = "FIRST_MATCH_RESULT_RELEASE",
    FIRST_MATCH_CONFIRM_END = "FIRST_MATCH_CONFIRM_END",
    SECOND_MATCH_RESULT_RELEASE = "SECOND_MATCH_RESULT_RELEASE",

    ACTIVITY_START = "ACTIVITY_START",

    EXIT_QUESTIONNAIRE_RELEASE = "EXIT_QUESTIONNAIRE_RELEASE",
    EXIT_QUESTIONNAIRE_END = "EXIT_QUESTIONNAIRE_END",
}

export const userState = ref<UserStates>(UserStates.UNKNOWN);
export const nextStatusChange = ref<Date | null>(null);
export const nextStatusCountdown = ref<string | null>(null);
export const nextStatusDeadlineReached = ref<boolean>(false);

export const fetchUserState = async () => {
    const response = await get("status/");
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to get user state");
    }
    const data = await response.json();
    const deadline = new Date(data.data.deadline*1000);
    const status = data.data.status;
    userState.value = UserStates[status as keyof typeof UserStates];
    nextStatusChange.value = new Date(data.data.deadline*1000);
    updateCountdown();
    console.log("fetchUserState", userState.value, nextStatusChange.value, nextStatusCountdown.value);
}

export const lazyFetchUserState = async () => {
    if (userState.value === UserStates.UNKNOWN || userState.value === UserStates.MAINTENANCE) {
        try {
            await fetchUserState();
        } catch (error) {
            console.error("lazyFetchUserState", error);
        }
    }
}

const updateCountdown = () => {
    if (nextStatusChange.value) {
        const now = new Date();
        const diff = nextStatusChange.value.getTime() - now.getTime();
        
        if (diff <= 0) {
            nextStatusCountdown.value = "已到期";
            nextStatusDeadlineReached.value = true;
            return;
        }
        
        // Convert milliseconds to days, hours, minutes, seconds
        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((diff % (1000 * 60)) / 1000);
        
        // Format the countdown string
        const parts = [];
        if (days > 0) parts.push(`${days}天`);
        if (hours > 0 || days > 0) parts.push(`${hours}时`);
        if (minutes > 0 || hours > 0 || days > 0) parts.push(`${minutes}分`);
        parts.push(`${seconds}秒`);
        const filteredParts = parts.slice(0, 2);
        
        nextStatusCountdown.value = filteredParts.join(' ');
    }
}

setInterval(() => {
    updateCountdown();
}, 1000);