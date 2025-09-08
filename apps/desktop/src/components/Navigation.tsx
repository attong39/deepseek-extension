/**
 * Navigation Component
 * ===================
 * 
 * Top navigation bar for agent management application.
 * Provides routing between different sections.
 */

import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Users, GitBranch, BarChart3, Zap } from 'lucide-react';
import Agent from "Agent";
import Backend from "Backend";
import Component from "Component";
import Connected from "Connected";
import Explore from "Explore";
import FC from "FC";
import Graph from "Graph";
import Icon from "Icon";
import Indicator from "Indicator";
import Items from "Items";
import Knowledge from "Knowledge";
import Logo from "Logo";
import Manage from "Manage";
import Metrics from "Metrics";
import Multi from "Multi";
import Navigation from "./Navigation";
import Orchestration from "Orchestration";
import Performance from "Performance";
import Platform from "Platform";
import Provides from "Provides";
import Status from "../pages/Status";
import Teams from "Teams";
import Top from "Top";
import Zeta from "Zeta";

const Navigation: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const navigationItems = [
    {
      path: '/agents',
      label: 'Agent Teams',
      icon: Users,
      description: 'Manage multi-agent teams'
    },
    {
      path: '/knowledge',
      label: 'Knowledge Graph',
      icon: GitBranch,
      description: 'Explore entity relationships'
    },
    {
      path: '/metrics',
      label: 'Metrics',
      icon: BarChart3,
      description: 'Performance monitoring'
    }
  ];

  const isActive = (path: string) => location.pathname === path;

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-white border-b border-gray-200 shadow-sm">
      <div className="container mx-auto px-6">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center gap-2">
            <div className="bg-blue-600 p-2 rounded-lg">
              <Zap className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">Zeta Agent Platform</h1>
              <p className="text-xs text-gray-500">Multi-Agent Orchestration</p>
            </div>
          </div>

          {/* Navigation Items */}
          <div className="flex items-center space-x-1">
            {navigationItems.map((item) => {
              const Icon = item.icon;
              return (
                <button
                  key={item.path}
                  onClick={() => navigate(item.path)}
                  className={`
                    flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all
                    ${isActive(item.path)
                      ? 'bg-blue-100 text-blue-700 shadow-sm'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                    }
                  `}
                  title={item.description}
                >
                  <Icon className="h-4 w-4" />
                  {item.label}
                </button>
              );
            })}
          </div>

          {/* Status Indicator */}
          <div className="flex items-center gap-2">
            <div className="flex items-center gap-1 text-xs text-gray-500">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              Backend Connected
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
