// posthog.js

import posthog from 'posthog-js';

posthog.init('phc_riCzwyMkRO7qRnhNLYfUIAehPc6V0U7Qudkv1a1XLu0', { api_host: 'https://eu.i.posthog.com', person_profiles: 'always', disable_web_experiments: false  });

// Define plan prices
const planPrices = {
    'FREE': 0,
    'PREMIUM': 9.99,
    'MAX-IMAL': 19.99
};

// Track page views
posthog.capture('$pageview');

// Example of tracking a custom event
function trackButtonClick(buttonName) {
    posthog.capture('button_clicked', { button_name: buttonName });
}

// Identify user after login or signup
function identifyUser(userEmail) {
    posthog.identify(userEmail);
}

// Track plan selection
function trackPlanSelection(planName) {
    const normalizedPlanName = planName.toUpperCase();
    posthog.capture('plan_selected', {
        plan_name: normalizedPlanName,
        plan_price: planPrices[normalizedPlanName] || 'Unknown'
    });
}

// Track plan purchase
function trackPlanPurchase(planName) {
    const normalizedPlanName = planName.toUpperCase();
    posthog.capture('plan_purchased', {
        plan_name: normalizedPlanName,
        plan_price: planPrices[normalizedPlanName] || 'Unknown'
    });
}

// Export functions for use in other scripts
export { trackButtonClick, identifyUser, trackPlanSelection, trackPlanPurchase };