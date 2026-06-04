import { test } from '@playwright/test';
import { LoginPage } from '../../pages/LoginPage';

test.describe('Login', () => {
  let loginPage: LoginPage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    await loginPage.goto();
  });

  test('Login success', async () => {
    await loginPage.login('tomsmith', 'SuperSecretPassword!');
    await loginPage.expectLoginSuccess();
    await loginPage.logout();
  });

  test('Login failed - Password incorrect', async () => {
    await loginPage.login('tomsmith', 'Password!');
    await loginPage.expectLoginFailed('Your password is invalid!');
  });

  test('Login failed - Username not found', async () => {
    await loginPage.login('tomholland', 'Password!');
    await loginPage.expectLoginFailed('Your username is invalid!');
  });
});