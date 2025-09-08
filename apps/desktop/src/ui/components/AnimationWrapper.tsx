import { HTMLMotionProps, motion, Variants } from 'framer-motion';
import React from 'react';
import Animation from "Animation";
import AnimationWrapper from "./AnimationWrapper";
import AnimationWrapperProps from "AnimationWrapperProps";
import Children from "Children";
import Cung from "Cung";
import Custom from "Custom";
import Delay from "Delay";
import FC from "FC";
import Fade from "Fade";
import Framer from "Framer";
import Get from "Get";
import ItemComponent from "ItemComponent";
import List from "List";
import Modal from "./Modal";
import ModalTransition from "ModalTransition";
import Motion from "Motion";
import Override from "Override";
import Page from "Page";
import PageTransition from "PageTransition";
import Predefined from "Predefined";
import ReactNode from "ReactNode";
import Specialized from "Specialized";
import Stagger from "Stagger";
import StaggerList from "StaggerList";
import Whether from "Whether";
import YourComponent from "YourComponent";

// Predefined animation variants
export const fadeInVariants: Variants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { duration: 0.3 } },
  exit: { opacity: 0, transition: { duration: 0.2 } }
};

export const slideInVariants: Variants = {
  hidden: { x: -50, opacity: 0 },
  visible: { x: 0, opacity: 1, transition: { duration: 0.4, ease: 'easeOut' } },
  exit: { x: 50, opacity: 0, transition: { duration: 0.3 } }
};

export const scaleInVariants: Variants = {
  hidden: { scale: 0.8, opacity: 0 },
  visible: { scale: 1, opacity: 1, transition: { duration: 0.3, ease: 'easeOut' } },
  exit: { scale: 0.8, opacity: 0, transition: { duration: 0.2 } }
};

export const staggerContainerVariants: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.1
    }
  }
};

export const staggerItemVariants: Variants = {
  hidden: { y: 20, opacity: 0 },
  visible: { y: 0, opacity: 1, transition: { duration: 0.3 } }
};

export interface AnimationWrapperProps extends HTMLMotionProps<'div'> {
  /** Animation variant preset */
  variant?: 'fadeIn' | 'slideIn' | 'scaleIn' | 'stagger';
  /** Custom animation variants */
  customVariants?: Variants;
  /** Whether animation should play on mount */
  animate?: boolean;
  /** Delay before animation starts (in seconds) */
  delay?: number;
  /** Animation duration override (in seconds) */
  duration?: number;
  /** Children to animate */
  children: React.ReactNode;
  /** Whether to use exit animations */
  enableExit?: boolean;
}

/**
 * Animation wrapper component sử dụng Framer Motion
 * Cung cấp predefined animations và custom animation support
 * 
 * @example
 * // Fade in animation
 * <AnimationWrapper variant="fadeIn">
 *   <YourComponent />
 * </AnimationWrapper>
 * 
 * @example
 * // Stagger animation for lists
 * <AnimationWrapper variant="stagger">
 *   {items.map(item => (
 *     <AnimationWrapper key={item.id} variant="fadeIn">
 *       <ItemComponent item={item} />
 *     </AnimationWrapper>
 *   ))}
 * </AnimationWrapper>
 * 
 * @example
 * // Custom animation
 * <AnimationWrapper
 *   customVariants={{
 *     hidden: { rotate: -180, scale: 0 },
 *     visible: { rotate: 0, scale: 1 }
 *   }}
 * >
 *   <YourComponent />
 * </AnimationWrapper>
 */
export const AnimationWrapper: React.FC<AnimationWrapperProps> = ({
  variant = 'fadeIn',
  customVariants,
  animate = true,
  delay = 0,
  duration,
  children,
  enableExit = false,
  ...motionProps
}) => {
  // Get predefined variants
  const getVariants = (): Variants => {
    if (customVariants) return customVariants;
    
    switch (variant) {
      case 'slideIn':
        return slideInVariants;
      case 'scaleIn':
        return scaleInVariants;
      case 'stagger':
        return staggerContainerVariants;
      default:
        return fadeInVariants;
    }
  };

  // Override timing if specified
  const variants = React.useMemo(() => {
    const baseVariants = getVariants();
    
    if (!duration && !delay) return baseVariants;
    
    return Object.entries(baseVariants).reduce((acc, [key, value]) => {
      if (typeof value === 'object' && value !== null && 'transition' in value) {
        const animationValue = value as { transition: object };
        acc[key] = {
          ...value,
          transition: {
            ...animationValue.transition,
            ...(duration && { duration }),
            ...(delay && { delay })
          }
        };
      } else {
        acc[key] = value;
      }
      return acc;
    }, {} as Variants);
  }, [duration, delay, variant, customVariants]);

  return (
    <motion.div
      variants={variants}
      initial="hidden"
      animate={animate ? "visible" : "hidden"}
      exit={enableExit ? "exit" : undefined}
      {...motionProps}
    >
      {children}
    </motion.div>
  );
};

// Specialized animation components for common use cases

/**
 * Page transition wrapper
 */
export const PageTransition: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <AnimationWrapper variant="fadeIn" duration={0.2} enableExit>
    {children}
  </AnimationWrapper>
);

/**
 * Modal transition wrapper
 */
export const ModalTransition: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <AnimationWrapper variant="scaleIn" duration={0.25} enableExit>
    {children}
  </AnimationWrapper>
);

/**
 * List item stagger animation
 */
export const StaggerList: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <AnimationWrapper variant="stagger">
    {React.Children.map(children, (child) => (
      <motion.div variants={staggerItemVariants}>
        {child}
      </motion.div>
    ))}
  </AnimationWrapper>
);

export default AnimationWrapper;
