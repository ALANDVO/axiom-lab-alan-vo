import { render, screen } from '@testing-library/react';
import { vi, describe, it, expect } from 'vitest';
import { ProfilePage } from './ProfilePage';

describe('ProfilePage', () => {
  it('renders without crashing', () => {
    const { container } = render(<ProfilePage />);
    const h1 = container.querySelector('h1');
    expect(h1).toBeInTheDocument();
    expect(h1?.textContent).toContain('Candidate Profile');
  });

  it('shows 0% completeness initially', () => {
    render(<ProfilePage />);
    const percentSpans = screen.getAllByText(/0%/);
    expect(percentSpans.length).toBeGreaterThan(0);
    // The completeness percentage should be inside an h2
    const h2WithPercent = percentSpans.find(s => s.closest('h2'));
    expect(h2WithPercent).toBeInTheDocument();
  });

  it('shows profile form elements exist', () => {
    render(<ProfilePage />);
    
    // Form labels and inputs exist in the DOM
    const pageContent = document.body.innerHTML;
    expect(pageContent).toContain('Candidate Profile');
    expect(pageContent).toContain('Name');
    expect(pageContent).toContain('Current Role');
    expect(pageContent).toContain('Location');
    expect(pageContent).toContain('Skills');
    expect(pageContent).toContain('Experience');
    expect(pageContent).toContain('Education');
    expect(pageContent).toContain('Contacts');
    expect(pageContent).toContain('Screening');
    expect(pageContent).toContain('Settings');
  });

  it('completeness increases when name is filled', () => {
    render(<ProfilePage />);
    // Use a more specific query - find the input by its placeholder or role
    const nameInput = screen.getByRole('textbox', { name: /name/i });
    nameInput.dispatchEvent(new Event('input', { bubbles: true }));
    nameInput.value = 'Alan Vo';
    nameInput.dispatchEvent(new Event('input', { bubbles: true }));
    
    const percentSpans = screen.getAllByText(/15%/);
    expect(percentSpans.length).toBeGreaterThan(0);
  });

  it('completeness increases when role is filled', () => {
    render(<ProfilePage />);
    const roleInput = screen.getByRole('textbox', { name: /current role|role/i });
    roleInput.dispatchEvent(new Event('input', { bubbles: true }));
    roleInput.value = 'Software Engineer';
    roleInput.dispatchEvent(new Event('input', { bubbles: true }));
    
    const percentSpans = screen.getAllByText(/25%/);
    expect(percentSpans.length).toBeGreaterThan(0);
  });

  it('completeness reaches higher percentage with more fields filled', () => {
    render(<ProfilePage />);
    
    const nameInput = screen.getByRole('textbox', { name: /name/i });
    nameInput.dispatchEvent(new Event('input', { bubbles: true }));
    nameInput.value = 'Alan Vo';
    nameInput.dispatchEvent(new Event('input', { bubbles: true }));
    
    const roleInput = screen.getByRole('textbox', { name: /current role|role/i });
    roleInput.dispatchEvent(new Event('input', { bubbles: true }));
    roleInput.value = 'Software Engineer';
    roleInput.dispatchEvent(new Event('input', { bubbles: true }));
    
    const locationInput = screen.getByRole('textbox', { name: /location/i });
    locationInput.dispatchEvent(new Event('input', { bubbles: true }));
    locationInput.value = 'San Francisco, CA';
    locationInput.dispatchEvent(new Event('input', { bubbles: true }));
    
    const percentSpans = screen.getAllByText(/40%|50%|60%|70%|80%|100%/);
    expect(percentSpans.length).toBeGreaterThan(0);
  });
});
