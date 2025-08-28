// images.ts

// --- Main Packages ---
import babyShowerPackage from '../assets/images/baby-shower-package.jpeg';
import birthdayPackage from '../assets/images/birthday-package.jpeg';
import corporatePackage from '../assets/images/corporate-package.jpeg';
import weddingPackage from '../assets/images/wedding-package.jpeg';
import customWoodSign from '../assets/images/custom-wood-sign-package.jpeg';
import christeningPackage from '../assets/images/christening-package.jpeg';
import engagementPackage from '../assets/images/engagement-package.jpeg';
import genderRevealPackage from '../assets/images/gender-reveal-package.jpeg';
import numberPackage from '../assets/images/number-package.jpeg';
import retirementPackage from '../assets/images/retirement-package.jpeg';
import anniversaryPackage from '../assets/images/anniversary-package.jpeg';

// --- Numbers examples ---
import NinePinkGreen from '../assets/images/9-pink-green.jpeg';
import ThirteenGoldBlack from '../assets/images/13-gold-black.jpeg';
import TwentySixWhiteYellow from '../assets/images/26-white-yellow.jpeg';
import SixtyNavy from '../assets/images/60-navy.jpeg';
import SeventyRedMetallic from '../assets/images/70-red-metallic.jpeg';

// --- Other occasion ---

// --- Decorations (commented out until you have assets) ---
// import shimmerWallGold from '../assets/images/shimmer-wall-gold.jpeg';
// import neonSignLove from '../assets/images/neon-sign-love.jpeg';
// import balloonArchClassic from '../assets/images/balloon-arch-classic.jpeg';

type Category =
  | 'Weddings'
  | 'Anniversaries'
  | 'Birthdays'
  | 'Corporate'
  | 'Baby-Showers'
  | 'Christenings'
  | 'Engagements'
  | 'Gender-Reveals'
  | 'Retirements'
  | 'Parties'
  | 'Decorations'
  | 'Custom';

interface ImageMeta {
  title: string;
  category: Category;
  src: string;
  alt: string;
}

export const IMAGES: Record<string, ImageMeta> = {
  // --- Weddings & Anniversaries ---
  weddingPackage: {
    title: 'Wedding Package',
    category: 'Weddings',
    src: (weddingPackage as any)?.src ?? (weddingPackage as string),
    alt: 'Elegant wedding backdrop with balloons and florals',
  },
  anniversaryPackage: {
    title: 'Anniversary Package',
    category: 'Anniversaries',
    src: (anniversaryPackage as any)?.src ?? (anniversaryPackage as string),
    alt: 'Anniversary party balloon display with elegant decor',
  },
  engagementPackage: {
    title: 'Engagement Package',
    category: 'Weddings',
    src: (engagementPackage as any)?.src ?? (engagementPackage as string),
    alt: 'Engagement party balloon display with romantic tones',
  },

  // --- Birthdays & Parties ---
  birthdayPackage: {
    title: 'Birthday Package',
    category: 'Birthdays',
    src: (birthdayPackage as any)?.src ?? (birthdayPackage as string),
    alt: 'Birthday party backdrop decorated with balloons and signage',
  },
  numberPackage: {
    title: '4ft LED Numbers',
    category: 'Birthdays',
    src: (numberPackage as any)?.src ?? (numberPackage as string),
    alt: 'Number balloon display for milestone birthdays or events',
  },
  ninePinkGreen: {
    title: '9 — Pink & Green',
    category: 'Birthdays',
    src: (NinePinkGreen as any)?.src ?? (NinePinkGreen as string),
    alt: 'Number 9 display styled in pink and green',
  },
  thirteenGoldBlack: {
    title: '13 — Gold & Black',
    category: 'Birthdays',
    src: (ThirteenGoldBlack as any)?.src ?? (ThirteenGoldBlack as string),
    alt: 'Number 13 display in gold and black styling',
  },
  twentySixWhiteYellow: {
    title: '26 — White & Yellow',
    category: 'Birthdays',
    src: (TwentySixWhiteYellow as any)?.src ?? (TwentySixWhiteYellow as string),
    alt: 'Number 26 display in white and yellow',
  },
  sixtyNavy: {
    title: '60 — Navy Theme',
    category: 'Birthdays',
    src: (SixtyNavy as any)?.src ?? (SixtyNavy as string),
    alt: 'Number 60 display with navy theme',
  },
  seventyRedMetallic: {
    title: '70 — Red Metallic',
    category: 'Birthdays',
    src: (SeventyRedMetallic as any)?.src ?? (SeventyRedMetallic as string),
    alt: 'Number 70 display with red metallic balloons',
  },

  // --- Corporate ---
  corporatePackage: {
    title: 'Corporate Package',
    category: 'Corporate',
    src: (corporatePackage as any)?.src ?? (corporatePackage as string),
    alt: 'Corporate event backdrop with balloon arch and branding',
  },

  // --- Baby Showers & Christenings ---
  babyShowerPackage: {
    title: 'Baby Shower Package',
    category: 'Baby-Showers',
    src: (babyShowerPackage as any)?.src ?? (babyShowerPackage as string),
    alt: 'Baby shower balloon and floral setup with pastel decorations',
  },
  christeningPackage: {
    title: 'Christening Package',
    category: 'Christenings',
    src: (christeningPackage as any)?.src ?? (christeningPackage as string),
    alt: 'Christening balloon arch with greenery and floral accents',
  },
  genderRevealPackage: {
    title: 'Gender Reveal Package',
    category: 'Gender-Reveals',
    src: (genderRevealPackage as any)?.src ?? (genderRevealPackage as string),
    alt: 'Gender reveal balloon package in pink and blue theme',
  },

  // --- Retirements ---
  retirementPackage: {
    title: 'Retirement Package',
    category: 'Retirements',
    src: (retirementPackage as any)?.src ?? (retirementPackage as string),
    alt: 'Retirement celebration backdrop with balloons and florals',
  },

  // --- Decorations (commented out until images are added) ---
  // shimmerWallGold: {
  //   title: 'Shimmer Wall — Gold',
  //   category: 'Decorations',
  //   src: (shimmerWallGold as any)?.src ?? (shimmerWallGold as string),
  //   alt: 'Gold shimmer wall decoration for events',
  // },
  // neonSignLove: {
  //   title: 'Neon Sign — Love',
  //   category: 'Decorations',
  //   src: (neonSignLove as any)?.src ?? (neonSignLove as string),
  //   alt: 'LED neon sign displaying the word "Love"',
  // },
  // balloonArchClassic: {
  //   title: 'Balloon Arch — Classic',
  //   category: 'Decorations',
  //   src: (balloonArchClassic as any)?.src ?? (balloonArchClassic as string),
  //   alt: 'Classic balloon arch in pastel colours',
  // },

  // --- Custom ---
  customWoodSign: {
    title: 'Customised Wooden Signs',
    category: 'Custom',
    src: (customWoodSign as any)?.src ?? (customWoodSign as string),
    alt: 'Custom engraved wooden event sign for personalisation',
  },
};
