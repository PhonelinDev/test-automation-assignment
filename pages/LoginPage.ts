import { Page, expect } from '@playwright/test';

export class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('http://the-internet.herokuapp.com/login');
  }

  async login(username: string, password: string) {
    await this.page.getByLabel('Username').fill(username);
    await this.page.getByLabel('Password').fill(password);
    await this.page.getByRole('button', { name: 'Login' }).click();
  }

  async expectLoginSuccess() {
    await expect(this.page.locator('.flash.success')).toBeVisible({ timeout: 10000 });
  }

  async expectLoginFailed(message: string) {
    await expect(this.page.locator('.flash.error')).toContainText(message, { timeout: 10000 });
  }

  async logout() {
    await this.page.getByRole('link', { name: 'Logout' }).click();
  }
}