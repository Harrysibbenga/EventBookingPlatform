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
import proposalPackage from '../assets/images/proposal-package.jpeg';

// --- Numbers examples ---
import NinePinkGreen from '../assets/images/9-pink-green.jpeg';
import ThirteenGoldBlack from '../assets/images/13-gold-black.jpeg';
import TwentySixWhiteYellow from '../assets/images/26-white-yellow.jpeg';
import SixtyNavy from '../assets/images/60-navy.jpeg';
import SeventyRedMetallic from '../assets/images/70-red-metallic.jpeg';
import OneInAMillion from '../assets/images/one-in-a-minion.jpeg';
import TwoCute from '../assets/images/two-cute.jpeg';
import TwoSweet from '../assets/images/two-sweet.jpeg';
import YoungWildThree from '../assets/images/young-wild-and-three.jpeg';
import FourEverYoung from '../assets/images/four-ever-young.jpeg';
import HighFve from '../assets/images/high-five.jpeg';
import Sixziller from '../assets/images/sixziller.jpeg';
import LuckyNumberSeven from '../assets/images/lucky-number-seven.jpeg';
import PirEights from '../assets/images/pir-eights.jpeg';
import CloudNine from '../assets/images/cloud-nine.jpeg';
import TenOutOfTen from '../assets/images/ten-out-of-ten.jpeg';
import TenPocalypse from '../assets/images/10-pocalypse.jpeg';



// --- Wedding ---
import JustMarriedGreenWhite from '../assets/images/just-married-green-white.jpeg';
import WeddingMrandMrs from '../assets/images/wedding-mr-and-mrs.jpeg';

// Halloween
import boo from '../assets/images/boo.jpeg';
import bewareTheUndead from '../assets/images/beware-the-undead.jpeg';
import enterIfYouDare from '../assets/images/enter-if-you-dare.jpeg';
import frightNight from '../assets/images/fright-night.jpeg';
import halloweenBlackOrange from '../assets/images/halloween-black-orange.jpeg';
import lockedUp from '../assets/images/locked-up.jpeg';
import PumpkinPatch from '../assets/images/pumpkin-patch.jpeg';
import RestingWitchFace from '../assets/images/resting-witch-face.jpeg';
import TheEndIsNear from '../assets/images/the-end-is-near.jpeg';
import TrickOrTreat from '../assets/images/trick-or-treat-black-green.jpeg';

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
  | 'Retirements'
  | 'Proposals'
  | 'Halloween'
  | 'Numbers'
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
  JustMarriedGreenWhite: {
    title: 'Just Married — Green & White',
    category: 'Weddings',
    src: (JustMarriedGreenWhite as any)?.src ?? (JustMarriedGreenWhite as string),
    alt: 'Just Married balloon display in green and white theme',
  },
  WeddingMrandMrs: {
    title: 'Mr & Mrs — Pink & Gold',
    category: 'Weddings',
    src: (WeddingMrandMrs as any)?.src ?? (WeddingMrandMrs as string),
    alt: 'Mr & Mrs balloon display in pink and gold theme',
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

  // --- Proposals ---
  proposalPackage: {
    title: 'Proposal Package',
    category: 'Proposals',
    src: (proposalPackage as any)?.src ?? (proposalPackage as string),
    alt: 'Romantic proposal setup with balloons and floral decorations',
  },

  // -- Halloween ---
  boo: {
    title: 'Boo',
    category: 'Halloween',
    src: (boo as any)?.src ?? (boo as string),
    alt: 'Halloween balloon display with spooky "Boo" sign',
  },
  bewareTheUndead: {
    title: 'Beware the Undead',
    category: 'Halloween',
    src: (bewareTheUndead as any)?.src ?? (bewareTheUndead as string),
    alt: 'Spooky Halloween balloon display with "Beware the Undead" sign',
  },
  enterIfYouDare: {
    title: 'Enter If You Dare',
    category: 'Halloween',
    src: (enterIfYouDare as any)?.src ?? (enterIfYouDare as string),
    alt: 'Creepy Halloween balloon display with "Enter If You Dare" sign',
  },
  frightNight: {
    title: 'Fright Night',
    category: 'Halloween',
    src: (frightNight as any)?.src ?? (frightNight as string),
    alt: 'Spooky Halloween balloon display with "Fright Night" sign',
  },
  halloweenBlackOrange: {
    title: 'Halloween — Black & Orange',
    category: 'Halloween',
    src: (halloweenBlackOrange as any)?.src ?? (halloweenBlackOrange as string),
    alt: 'Halloween balloon display in black and orange theme',
  },
  lockedUp: {
    title: 'Locked Up',
    category: 'Halloween',
    src: (lockedUp as any)?.src ?? (lockedUp as string),
    alt: 'Spooky Halloween balloon display with "Locked Up" sign',
  },
  pumpkinPatch: {
    title: 'Pumpkin Patch',
    category: 'Halloween',
    src: (PumpkinPatch as any)?.src ?? (PumpkinPatch as string),
    alt: 'Festive Halloween balloon display with pumpkins',
  },
  restingWitchFace: {
    title: 'Resting Witch Face',
    category: 'Halloween',
    src: (RestingWitchFace as any)?.src ?? (RestingWitchFace as string),
    alt: 'Humorous Halloween balloon display with "Resting Witch Face" sign',
  },
  theEndIsNear: {
    title: 'The End is Near',
    category: 'Halloween',
    src: (TheEndIsNear as any)?.src ?? (TheEndIsNear as string),
    alt: 'Spooky Halloween balloon display with "The End is Near" sign',
  },
  trickOrTreat: {
    title: 'Trick or Treat — Black & Green',
    category: 'Halloween',
    src: (TrickOrTreat as any)?.src ?? (TrickOrTreat as string),
    alt: 'Halloween balloon display in black and green theme with "Trick or Treat" sign',
  },

  // --- Numbers ---
  oneInAMillion: {
    title: 'One in a Million',
    category: 'Numbers',
    src: (OneInAMillion as any)?.src ?? (OneInAMillion as string),
    alt: 'Number balloon display with "One in a Million" sign',
  },
  twoCute: {
    title: 'Two Cute',
    category: 'Numbers',
    src: (TwoCute as any)?.src ?? (TwoCute as string),
    alt: 'Number 2 balloon display with "Two Cute" sign',
  },
  twoSweet: {
    title: 'Two Sweet',
    category: 'Numbers',
    src: (TwoSweet as any)?.src ?? (TwoSweet as string),
    alt: 'Number 2 balloon display with "Two Sweet" sign',
  },
  youngWildThree: {
    title: 'Young, Wild & Three',
    category: 'Numbers',
    src: (YoungWildThree as any)?.src ?? (YoungWildThree as string),
    alt: 'Number 3 balloon display with "Young, Wild & Three" sign',
  },
  fourEverYoung: {
    title: 'Four Ever Young',
    category: 'Numbers',
    src: (FourEverYoung as any)?.src ?? (FourEverYoung as string),
    alt: 'Number 4 balloon display with "Four Ever Young" sign',
  },
  highFve: {
    title: 'High Fve',
    category: 'Numbers',
    src: (HighFve as any)?.src ?? (HighFve as string),
    alt: 'Number 5 balloon display with "High Fve" sign',
  },
  sixziller: {
    title: 'Sixziller',
    category: 'Numbers',
    src: (Sixziller as any)?.src ?? (Sixziller as string),
    alt: 'Number 6 balloon display with "Sixziller" sign',
  },
  luckyNumberSeven: {
    title: 'Lucky Number Seven',
    category: 'Numbers',
    src: (LuckyNumberSeven as any)?.src ?? (LuckyNumberSeven as string),
    alt: 'Number 7 balloon display with "Lucky Number Seven" sign',
  },
  pirEights: {
    title: 'Pir-Eights',
    category: 'Numbers',
    src: (PirEights as any)?.src ?? (PirEights as string),
    alt: 'Number 8 balloon display with "Pir-Eights" sign',
  },
  cloudNine: {
    title: 'Cloud Nine',
    category: 'Numbers',
    src: (CloudNine as any)?.src ?? (CloudNine as string),
    alt: 'Number 9 balloon display with "Cloud Nine" sign',
  },
  tenOutOfTen: {
    title: 'Ten Out of Ten',
    category: 'Numbers',
    src: (TenOutOfTen as any)?.src ?? (TenOutOfTen as string),
    alt: 'Number 10 balloon display with "Ten Out of Ten" sign',
  },
  tenPocalypse: {
    title: '10-Pocalypse',
    category: 'Numbers',
    src: (TenPocalypse as any)?.src ?? (TenPocalypse as string),
    alt: 'Number 10 balloon display with "10-Pocalypse" sign',
  },

  // --- Custom ---
  customWoodSign: {
    title: 'Customised Wooden Signs',
    category: 'Custom',
    src: (customWoodSign as any)?.src ?? (customWoodSign as string),
    alt: 'Custom engraved wooden event sign for personalisation',
  },
};
