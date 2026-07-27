import { useEffect, useState } from "react";

export default function GlobalErrorBanner() {
  const [banner, setBanner] = useState(null);

  useEffect(() => {
    let timerId;
    const handler = (event) => {
      const message = event?.detail?.message || "Something went wrong.";
      setBanner(message);
      clearTimeout(timerId);
      timerId = setTimeout(() => setBanner(null), 4500);
    };

    window.addEventListener("api-error", handler);
    return () => {
      clearTimeout(timerId);
      window.removeEventListener("api-error", handler);
    };
  }, []);

  if (!banner) return null;

  return (
    <div className="global-error-banner" role="alert">
      <span>{banner}</span>
      <button className="banner-close" onClick={() => setBanner(null)} aria-label="Dismiss error">
        x
      </button>
    </div>
  );
}

