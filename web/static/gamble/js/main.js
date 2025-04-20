document.addEventListener("DOMContentLoaded", function () {
    const tg = window.Telegram?.WebApp;
    if (!tg) return;

    const user = tg.initDataUnsafe?.user || {};
    document.getElementById("id_telegram_id").value = user.id || "";
    document.getElementById("id_telegram_username").value = user.username || "";

    // Отмечаем подписку, если Telegram позволяет
    document.getElementById("id_is_subscribed").value =
        tg.initDataUnsafe?.can_send_after ? "1" : "0";

    tg.ready();
    tg.expand();  // при желании
});