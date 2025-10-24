import React from 'react';
import { useTheme } from '../contexts/ThemeContext';
import { Sun, Moon, Package } from 'lucide-react';

const Header: React.FC = () => {
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="bg-secondary border-b border-color shadow">
      <div className="container py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Package className="w-8 h-8 text-accent-primary" />
            <div>
              <h1 className="text-xl font-bold text-primary">Wooden Cutting Plan Optimizer</h1>
              <p className="text-sm text-secondary">Greenstrand Packaging</p>
            </div>
          </div>
          <button
            onClick={toggleTheme}
            className="btn btn-secondary p-2"
            aria-label="Toggle theme"
          >
            {theme === 'light' ? (
              <Moon className="w-5 h-5" />
            ) : (
              <Sun className="w-5 h-5" />
            )}
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;