const puppeteer = require('puppeteer');

(async () => {
	const browser = await puppeteer.connect({
		browserURL: 'http://localhost:9222',
	});
	const pages = await browser.pages();
	// Identify your Twitch config page. You might filter pages by URL.
	const configPage = pages.find((p) =>
		p.url().includes('extension-live-configure')
	);

	if (configPage) {
		// When "9" is pressed, execute:
		await configPage.evaluate(() => {
			const button = document.querySelector('#myButton'); // update selector accordingly
			if (button) button.click();
		});
		console.log('Button clicked via remote debugging.');
	} else {
		console.log('Twitch config page not found.');
	}
	await browser.disconnect();
})();
