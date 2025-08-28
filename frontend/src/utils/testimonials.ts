// src/data/testimonials.ts

import ryanAvatar from '../assets/testemonials/review-ryan.jpeg';
import maisonAvatar from '../assets/testemonials/review-maison.jpeg';
import frankieAvatar from '../assets/testemonials/review-frankie.jpeg';
import paulAvatar from '../assets/testemonials/review-paul.jpeg';
import charlotteAvatar from '../assets/testemonials/review-charlotte.jpeg';
import kellieAvatar from '../assets/testemonials/review-kellie.jpeg';
import tanyaAvatar from '../assets/testemonials/review-tanya.jpeg';
import anupamaAvatar from '../assets/testemonials/review-anupama.jpeg';
import stuartAvatar from '../assets/testemonials/review-stuart.jpeg';
import clareAvatar from '../assets/testemonials/review-clare.jpeg';

const ryanAvatarSrc = ryanAvatar.src ?? (ryanAvatar as unknown as string);
const maisonAvatarSrc = maisonAvatar.src ?? (maisonAvatar as unknown as string);
const frankieAvatarSrc = frankieAvatar.src ?? (frankieAvatar as unknown as string);
const paulAvatarSrc = paulAvatar.src ?? (paulAvatar as unknown as string);
const charlotteAvatarSrc = charlotteAvatar.src ?? (charlotteAvatar as unknown as string);
const kellieAvatarSrc = kellieAvatar.src ?? (kellieAvatar as unknown as string);
const tanyaAvatarSrc = tanyaAvatar.src ?? (tanyaAvatar as unknown as string);
const anupamaAvatarSrc = anupamaAvatar.src ?? (anupamaAvatar as unknown as string);
const stuartAvatarSrc = stuartAvatar.src ?? (stuartAvatar as unknown as string);
const clareAvatarSrc = clareAvatar.src ?? (clareAvatar as unknown as string);

export type Testimonial = {
    id: number;
    name: string;          // anonymised label for now (e.g. “Facebook review — Aug 2024”)
    role?: string;         // short context (e.g. “40th Birthday Party”)
    avatar: string;        // local image path inside src/assets/testemonials
    content: string;       // the review text (lightly edited for clarity)
    avatar: string;        // local image path inside src/assets/testemonials,
    event?: string;        // optional: event title
    date?: string;         // ISO-like “YYYY-MM-DD” when known
    source?: 'Facebook' | 'Instagram' | 'Google' | 'Direct' | 'Other';
  };
  
  export const testimonials: readonly Testimonial[] = [
    {
      id: 1,
      name: 'Ryan Davis — Aug 2024',
      role: '40th Birthday Party',
      avatar: ryanAvatarSrc,
      content:
        "Great communication and professional service. The numbers looked great and arrived on time. They helped with decoration ideas and balloons—I'll be using them again for other parties. Thank you to the team!",
      rating: 5,
      event: '40th Birthday',
      date: '2024-08-23',
      source: 'Facebook'
    },
    {
      id: 2,
      name: 'Masion Seaber — Aug 2024',
      role: "Daughter’s Birthday",
      avatar: maisonAvatarSrc,
      content:
        'Thank you so much for making my daughter’s birthday one to remember. So happy with the arrangement—highly recommend and will be using again.',
      rating: 5,
      event: "Child's Birthday",
      date: '2024-08-16',
      source: 'Facebook'
    },
    {
      id: 3,
      name: 'Frankie Seaber — Aug 2024',
      role: 'Multiple Events',
      avatar: frankieAvatarSrc,
      content:
        'Highly recommend for all your party and special events. The team are very friendly, helpful and reliable. I have them booked for my next few celebrations—can’t wait!',
      rating: 5,
      event: 'Parties & Celebrations',
      date: '2024-08-13',
      source: 'Facebook'
    },
    {
      id: 4,
      name: 'Paul Blake — 2024',
      role: '30th Birthday Party',
      avatar: paulAvatarSrc,
      content:
        'We used Royal Events for a 30th birthday party. They arranged everything from start to finish—light‑up numbers, balloons, lights—the venue looked fantastic. Highly recommend.',
      rating: 5,
      event: '30th Birthday',
      date: '2024-07-20',
      source: 'Facebook'
    },
    {
      id: 5,
      name: 'Charlotte Matthews — Jun 2024',
      role: 'Balloon Arch & Numbers',
      avatar: charlotteAvatarSrc,
      content:
        'Thank you so much for the balloon arch and numbers! It looked amazing and is still up now. Such friendly, easy‑going people. Great quality and lovely team—would definitely recommend.',
      rating: 5,
      event: 'Party Display',
      date: '2024-06-17',
      source: 'Facebook'
    },
    {
      id: 6,
      name: 'Kellie Gower — Feb 2024',
      role: 'Quote to Collection',
      avatar: kellieAvatarSrc,
      content:
        'Great experience from quote to collection. Balloon arch and numbers looked amazing! Thank you.',
      rating: 5,
      event: 'Party Display',
      date: '2024-02-22',
      source: 'Facebook'
    },
    {
      id: 7,
      name: 'Tanya Glassett — 2024',
      role: 'Milton Keynes',
      avatar: tanyaAvatarSrc,
      content:
        'Fantastic service from start to finish. Absolutely stunning displays—would highly recommend and will definitely use again.',
      rating: 5,
      event: 'Event Styling',
      source: 'Facebook'
    },
    {
      id: 8,
      name: 'Anupama Kaveri — 2024',
      role: '2nd Birthday',
      avatar: anupamaAvatarSrc,
      content:
        'Thank you so much for the prettiest balloon arch with butterflies and shining number 2 for my daughter’s birthday. We loved it—made the celebration sparkle. Professional, thorough and so accommodating. Can’t wait to have you for our next celebrations!',
      rating: 5,
      event: 'Second Birthday',
      source: 'Facebook'
    },
    {
      id: 9,
      name: 'Stuart Pearce — Nov 2023',
      role: '30th Birthday Party',
      avatar: stuartAvatarSrc,
      content:
        'An amazing display for my wife’s 30th birthday party. Great communication and very friendly. Will definitely use again and would recommend.',
      rating: 5,
      event: '30th Birthday',
      date: '2023-11-16',
      source: 'Facebook'
    },
    {
      id: 10,
      name: 'Claire Lee — Jun 2024',
      role: 'Baby Shower',
      avatar: clareAvatarSrc,
      content:
        "Used this company for my baby shower and can’t thank them enough. Communication before the day was amazing. I’ll definitely be using you for our baby’s 1st birthday—thank you so much!",
      rating: 5,
      event: 'Baby Shower',
      date: '2024-06-15',
      source: 'Facebook'
    }
  ] as const;
  
  // Optional: a small, curated list for homepage carousels
  export const featuredTestimonials = testimonials.slice(0, 6) as readonly Testimonial[];

  export default testimonials;
  