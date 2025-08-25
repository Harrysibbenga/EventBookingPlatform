// packages.ts
import { IMAGES } from './images';

export const PACKAGES = {
  babyShowerPackage: {
    ...IMAGES.babyShowerPackage,
  },
  birthdayPackage: {
    ...IMAGES.birthdayPackage,
  },
  corporatePackage: {
    ...IMAGES.corporatePackage,
  },
  weddingPackage: {
    ...IMAGES.weddingPackage,
  },
  customWoodSign: {
    ...IMAGES.customWoodSign,
  },
  christeningPackage: {
    ...IMAGES.christeningPackage,
  },
  engagementPackage: {
    ...IMAGES.engagementPackage,
  },
  genderRevealPackage: {
    ...IMAGES.genderRevealPackage,
  },
  numberPackage: {
    ...IMAGES.numberPackage,
  },
  retirementPackage: {
    ...IMAGES.retirementPackage,
  },
  anniversaryPackage: {
    ...IMAGES.anniversaryPackage,
  },
} as const;
