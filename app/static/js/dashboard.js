const DASHBOARD_URL = "/api/dashboard/";

function formatTime(dateStr) {
    if (!dateStr) return "--:--";
    const d = new Date(dateStr);
    return d.toLocaleTimeString("fr-FR", { hour: "2-digit", minute: "2-digit" });
}

function formatDayLength(seconds) {
    if (!seconds && seconds !== 0) return "-- h --";
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    return `${h} h ${m.toString().padStart(2, "0")} min`;
}

function updateClock() {
    const now = new Date();
    const timeEl = document.getElementById("clock-time");
    const dateEl = document.getElementById("clock-date");

    if (!timeEl || !dateEl) return;

    timeEl.textContent = now.toLocaleTimeString("fr-FR", {
        hour: "2-digit",
        minute: "2-digit",
    });

    dateEl.textContent = now.toLocaleDateString("fr-FR", {
        weekday: "long",
        day: "2-digit",
        month: "long",
        year: "numeric",
    });
}

async function refreshDashboard() {
    const footerStatus = document.getElementById("footer-refresh-status");
    try {
        if (footerStatus) {
            footerStatus.textContent = "Actualisation en cours...";
        }

        const resp = await fetch(DASHBOARD_URL);
        if (!resp.ok) {
            throw new Error(`HTTP ${resp.status}`);
        }
        const data = await resp.json();

        const weather = data.weather;
        const eph = data.ephemerides;

        // Météo
        document.getElementById("weather-temp").textContent =
            Math.round(weather.temperature) + "°C";

        document.getElementById("weather-desc").textContent =
            weather.description || "";

        document.getElementById("weather-feels").textContent =
            weather.feels_like != null ? Math.round(weather.feels_like) + "°C" : "--°C";

        document.getElementById("weather-humidity").textContent =
            weather.humidity != null ? weather.humidity + " %" : "--%";

        document.getElementById("weather-pressure").textContent =
            weather.pressure != null ? weather.pressure + " hPa" : "-- hPa";

        document.getElementById("weather-wind").textContent =
            weather.wind_speed != null ? weather.wind_speed + " m/s" : "-- m/s";

        document.getElementById("weather-location").textContent =
            weather.location || "";
        document.getElementById("weather-updated").textContent =
            "Dernière mise à jour : " + formatTime(weather.timestamp);

        // Éphémérides
        document.getElementById("eph-sunrise").textContent = formatTime(
            `${eph.date}T${eph.sunrise}`
        );
        document.getElementById("eph-sunset").textContent = formatTime(
            `${eph.date}T${eph.sunset}`
        );
        document.getElementById("eph-daylength").textContent = formatDayLength(
            eph.day_length_seconds
        );
        document.getElementById("eph-moon").textContent =
            eph.moon_phase_label || "---";
        
        // News régionales
        const newsList = document.getElementById("news-list");
        if (newsList) {
            newsList.innerHTML = "";

            if (data.news && data.news.length > 0) {
                data.news.forEach((item) => {
                    const li = document.createElement("li");
                    li.className = "news-item";

                    const a = document.createElement("a");
                    a.href = item.url || "#";
                    a.target = "_blank";
                    a.rel = "noopener noreferrer";
                    a.textContent = item.title;

                    const meta = document.createElement("div");
                    meta.className = "news-meta";

                    const src = item.source ? new URL(item.source).hostname : "";
                    let parts = [];
                    if (src) parts.push(src);
                    if (item.published_at) {
                        const d = new Date(item.published_at);
                        parts.push(
                            d.toLocaleString("fr-FR", {
                                weekday: "short",
                                day: "2-digit",
                                month: "short",
                                hour: "2-digit",
                                minute: "2-digit",
                            })
                        );
                    }

                    meta.textContent = parts.join(" • ");

                    li.appendChild(a);
                    li.appendChild(meta);

                    newsList.appendChild(li);
                });
            } else {
                const li = document.createElement("li");
                li.className = "news-item news-placeholder";
                li.textContent = "Aucune actualité disponible.";
                newsList.appendChild(li);
            }
        }

        if (footerStatus) {
            const now = new Date();
            footerStatus.textContent =
                "Dernière actualisation : " +
                now.toLocaleTimeString("fr-FR", {
                    hour: "2-digit",
                    minute: "2-digit",
                });
        }
    } catch (err) {
        console.error("Erreur dashboard:", err);
        if (footerStatus) {
            footerStatus.textContent = "Erreur de mise à jour des données";
        }
    }
}

document.addEventListener("DOMContentLoaded", () => {
    updateClock();
    setInterval(updateClock, 1000);

    refreshDashboard();
    setInterval(refreshDashboard, 60 * 1000); // toutes les minutes
});
