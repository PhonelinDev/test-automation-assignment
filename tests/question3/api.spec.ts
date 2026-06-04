import { test, expect } from '@playwright/test';

const BASE_URL = 'https://reqres.in';
const API_KEY = 'free_user_3EejvKgl2FhCguguqKsq7YnYnAY';

test.describe('REST API - GET User', () => {

  test('Get user profile success', async ({ request }) => {
    const response = await request.get(`${BASE_URL}/api/users/12`, {
      headers: { 'x-api-key': API_KEY }
    });
    
    expect(response.status()).toBe(200);
    
    const body = await response.json();
    expect(body.data.id).toBe(12);
    expect(body.data.email).toBe('rachel.howell@reqres.in');
    expect(body.data.first_name).toBe('Rachel');
    expect(body.data.last_name).toBe('Howell');
    expect(body.data.avatar).toBe('https://reqres.in/img/faces/12-image.jpg');
  });

  test('Get user profile but user not found', async ({ request }) => {
    const response = await request.get(`${BASE_URL}/api/users/1234`, {
      headers: { 'x-api-key': API_KEY }
    });
    
    expect(response.status()).toBe(404);
    const body = await response.json();
    expect(body).toEqual({});
  });

});