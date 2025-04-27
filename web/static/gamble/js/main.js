document.addEventListener("DOMContentLoaded", function () {
    // Скрипт для инициализации Telegram данных
    const tg = window.Telegram?.WebApp;
    if (!tg) return;

    const user = tg.initDataUnsafe?.user || {};
    document.getElementById("id_telegram_id").value = user.id || "";
    document.getElementById("id_telegram_username").value = user.username || "";
    document.getElementById("id_is_subscribed").value = tg.initDataUnsafe?.can_send_after ? "1" : "0";

    tg.ready();
    tg.expand();

    document.getElementById("openGroupBtn")?.addEventListener("click", () => {
        const url = "https://t.me/restinternationall";
        try {
            if (tg?.openLink) {
                tg.openLink(url);
            } else {
                window.open(url, "_blank").focus();
            }
        } catch (error) {
            console.error("Error opening link:", error);
            window.location.href = url;
        }
    });
});


// document.addEventListener("DOMContentLoaded", function () {
//     'use strict';

//     // Конфигурация
//     const CONFIG = {
//         DEBUG: true, // Включим отладку для диагностики
//         TG_CHANNEL: "test_fields",
//         SELECTORS: {
//             TELEGRAM_ID: "#id_telegram_id",
//             TELEGRAM_USERNAME: "#id_telegram_username",
//             IS_SUBSCRIBED: "#id_is_subscribed",
//             BUTTON: "#openGroupBtn"
//         }
//     };

//     // Инициализация Telegram WebApp
//     function initTelegramWebApp() {
//         try {
//             const tg = window.Telegram?.WebApp;
//             if (!tg) {
//                 CONFIG.DEBUG && console.log("Telegram WebApp не обнаружен");
//                 return null;
//             }
//             tg.ready();
//             tg.expand();
//             return tg;
//         } catch (error) {
//             CONFIG.DEBUG && console.error("Ошибка инициализации Telegram:", error);
//             return null;
//         }
//     }

//     // Заполнение Telegram данных
//     function populateTelegramData(tg) {
//         try {
//             const user = tg?.initDataUnsafe?.user || {};
//             const elements = {
//                 id: document.querySelector(CONFIG.SELECTORS.TELEGRAM_ID),
//                 username: document.querySelector(CONFIG.SELECTORS.TELEGRAM_USERNAME),
//                 subscribed: document.querySelector(CONFIG.SELECTORS.IS_SUBSCRIBED)
//             };

//             if (elements.id) elements.id.value = user.id || "";
//             if (elements.username) elements.username.value = user.username || "";
//             if (elements.subscribed) {
//                 elements.subscribed.value = tg?.initDataUnsafe?.can_send_after ? "1" : "0";
//             }
//         } catch (error) {
//             CONFIG.DEBUG && console.error("Ошибка заполнения данных:", error);
//         }
//     }

//     // Обработчик клика по кнопке
//     function handleSubscribeButton(tg) {
//         try {
//             const button = document.querySelector(CONFIG.SELECTORS.BUTTON);
//             if (!button) {
//                 CONFIG.DEBUG && console.log("Кнопка подписки не найдена");
//                 return;
//             }

//             button.addEventListener("click", function (e) {
//                 e.preventDefault();
//                 const url = `https://t.me/${CONFIG.TG_CHANNEL}`;
//                 CONFIG.DEBUG && console.log("Попытка открыть URL:", url);

//                 try {
//                     if (tg?.openLink) {
//                         tg.openLink(url);
//                         CONFIG.DEBUG && console.log("Открытие через tg.openLink");
//                     } else if (window.open(url, "_blank")) {
//                         window.focus();
//                         CONFIG.DEBUG && console.log("Открытие в новой вкладке");
//                     } else {
//                         window.location.href = url;
//                         CONFIG.DEBUG && console.log("Перенаправление на URL");
//                     }
//                 } catch (error) {
//                     CONFIG.DEBUG && console.error("Ошибка открытия ссылки:", error);
//                     window.location.href = url;
//                 }
//             });
//         } catch (error) {
//             CONFIG.DEBUG && console.error("Ошибка в обработчике кнопки:", error);
//         }
//     }

//     // Основная инициализация
//     function main() {
//         const tg = initTelegramWebApp();
//         if (tg) populateTelegramData(tg);
//         handleSubscribeButton(tg);
//         console.log("Скрипт запущен");
//     }

//     // Запуск приложения
//     main();
// });