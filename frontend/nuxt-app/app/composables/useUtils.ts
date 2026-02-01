export const isWechat = computed(() => {
  var ua = window.navigator.userAgent.toLowerCase();
  if (ua.match(/MicroMessenger/i) !== null) {
    return true;
  } else {
    return false;
  }
});

export const isDarkMode = ref(false);
isDarkMode.value =
  window.matchMedia &&
  window.matchMedia("(prefers-color-scheme: dark)").matches;
window
  .matchMedia("(prefers-color-scheme: dark)")
  .addEventListener("change", (e) => {
    isDarkMode.value = e.matches;
  });


export interface VueformInstance {
  data: Record<string, any>;
  load(data: Record<string, any>): void;
  submitting: boolean;
}

export const getImageUrl = (path: string | null) => {
  if (!path) return '';
  if (path.startsWith('/')) {
    return `${API_HOST}${path}`;
  }
  return `${API_HOST}/media/${path}`;
};

export const compressImage = (file: File): Promise<Blob> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = (event) => {
      const img = new Image();
      img.src = event.target?.result as string;
      img.onload = () => {
        const canvas = document.createElement("canvas");
        const ctx = canvas.getContext("2d");
        const maxWidth = 1280;
        const maxHeight = 1280;
        let width = img.width;
        let height = img.height;

        if (width > height) {
          if (width > maxWidth) {
            height *= maxWidth / width;
            width = maxWidth;
          }
        } else {
          if (height > maxHeight) {
            width *= maxHeight / height;
            height = maxHeight;
          }
        }

        canvas.width = width;
        canvas.height = height;
        ctx?.drawImage(img, 0, 0, width, height);
        canvas.toBlob(
          (blob) => {
            if (blob) {
              resolve(blob);
            } else {
              reject(new Error("Image compression failed"));
            }
          },
          "image/jpeg",
          0.7
        );
      };
      img.onerror = (error) => reject(error);
    };
    reader.onerror = (error) => reject(error);
  });
};

export const getMBTIType = (mbti: { ei: number; sn: number; tf: number; jp: number } | null) => {
  if (!mbti) return '';
  const ei = mbti.ei >= 50 ? 'I' : 'E';
  const sn = mbti.sn >= 50 ? 'N' : 'S';
  const tf = mbti.tf >= 50 ? 'F' : 'T';
  const jp = mbti.jp >= 50 ? 'P' : 'J';
  return `${ei}${sn}${tf}${jp}`;
};