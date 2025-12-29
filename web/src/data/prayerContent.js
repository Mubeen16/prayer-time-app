export const prayerContent = {
    fajr: {
        title: "The Dawn Prayer",
        significance: "Fajr marks the beginning of the day. It is a time of purity and spiritual awakening. The Prophet (ﷺ) said: 'Two Rakahs of Fajr are better than the world and all that is in it.' (Muslim)",
        jurisprudence: "The time for Fajr begins at 'True Dawn' (Subh Sadiq) when a horizontal white light appears on the horizon and ends at sunrise.",
        limitations: "⚠️ Note on Calculation: In high-latitude regions (like the UK in summer), True Dawn may not occur as the sun doesn't dip far enough below the horizon. We use estimation methods (e.g., 1/7th of night) in these cases.",
        hadith: "The Angels of the night and the day meet at the Fajr prayer."
    },
    sunrise: {
        title: "Sunrise (Shuruq)",
        significance: "This is not a prayer time but the end of the Fajr time. It is forbidden to pray exactly as the sun rises.",
        jurisprudence: "Wait approx. 15-20 minutes after sunrise to offer Ishraq prayers.",
        limitations: null,
        hadith: null
    },
    zuhr: {
        title: "The Noon Prayer",
        significance: "Zuhr is the first prayer revealed to the Prophet (ﷺ) by Jibril (AS) after the night of Isra and Mi'raj. It offers a spiritual break in the middle of the work day.",
        jurisprudence: "Begins after the sun passes its zenith (highest point) and lasts until the shadow of an object equals its height (plus the shadow at zenith).",
        limitations: null,
        hadith: "The Gates of Heaven are opened during the time of Zuhr."
    },
    asr: {
        title: "The Afternoon Prayer",
        significance: "Asr is the 'Middle Prayer' (Salat al-Wusta) mentioned in the Quran. It is a time of heightened spiritual importance as the day winds down.",
        jurisprudence: "Major difference of opinion: \n• Standard (Shafi'i/Maliki/Hanbali): Shadow = Object Height.\n• Hanafi: Shadow = 2x Object Height. (We display Standard by default).",
        limitations: null,
        hadith: "Whoever misses the Asr prayer, it is as if he has lost his family and property."
    },
    maghrib: {
        title: "The Sunset Prayer",
        significance: "Maghrib must be hastened. It marks the end of the day and the beginning of the Islamic night.",
        jurisprudence: "Begins immediately after the sun sets (disk disappears) and lasts until the red twilight disappears.",
        limitations: "⚠️ Note on Calculation: Like Fajr, the 'disappearance of twilight' can be hard to calculate in high latitudes during summer. We rely on verified calculation methods to estimate this safely.",
        hadith: "My Ummah will remain in fine state as long as they hasten the Maghrib prayer."
    },
    isha: {
        title: "The Night Prayer",
        significance: "Isha is the final prayer of the day, offering peace before sleep. It is the specific gift of the Night Journey (Isra).",
        jurisprudence: "Begins when the red twilight disappears from the horizon and lasts until Fajr (preferred before midnight).",
        limitations: null,
        hadith: "Whoever prays Isha in congregation, it is as if he has stood half the night in prayer."
    },
    general: {
        miraj: {
            title: "The Gift of Salah (Isra & Mi'raj)",
            content: "The five daily prayers were ordained during the Prophet's (ﷺ) miraculous Night Journey (Isra) and Ascension (Mi'raj). Originally, Allah (SWT) commanded 50 prayers daily. On the advice of Prophet Musa (AS), the Prophet (ﷺ) returned to Allah multiple times to ask for a reduction, until it was set to 5 prayers. Allah (SWT) declared: 'They are five in action, but fifty in reward.' This highlights the immense value of each prayer time—it is a direct connection gifted from the Heavens."
        }
    }
};
