/**
 * AutoMaroc - Main JavaScript Application
 * Uses Alpine.js for reactivity
 */

// Alpine.js Data Components
document.addEventListener('alpine:init', () => {
    
    // Mobile Menu Component
    Alpine.data('mobileMenu', () => ({
        open: false,
        toggle() {
            this.open = !this.open
        },
        close() {
            this.open = false
        }
    }))
    
    // Car Gallery Component
    Alpine.data('carGallery', (images) => ({
        images: images || [],
        current: 0,
        
        init() {
            if (this.images.length === 0) {
                this.images = [{ url: '/static/images/car-placeholder.jpg', alt: 'No image' }]
            }
        },
        
        next() {
            this.current = (this.current + 1) % this.images.length
        },
        
        prev() {
            this.current = (this.current - 1 + this.images.length) % this.images.length
        },
        
        goTo(index) {
            this.current = index
        },
        
        get currentImage() {
            return this.images[this.current] || this.images[0]
        }
    }))
    
    // Car Filter Component
    Alpine.data('carFilters', () => ({
        open: false,
        
        toggle() {
            this.open = !this.open
        },
        
        reset() {
            window.location.href = window.location.pathname
        }
    }))
    
    // Toast Notifications
    Alpine.data('toast', () => ({
        messages: [],
        
        add(message, type = 'info') {
            const id = Date.now()
            this.messages.push({ id, message, type })
            
            setTimeout(() => {
                this.remove(id)
            }, 5000)
        },
        
        remove(id) {
            this.messages = this.messages.filter(m => m.id !== id)
        }
    }))
    
    // Image Lazy Loading
    Alpine.data('lazyImage', () => ({
        loaded: false,

        init() {
            const img = this.$el.querySelector('img')
            if (img) {
                img.addEventListener('load', () => {
                    this.loaded = true
                })

                // Trigger load if image is already cached
                if (img.complete) {
                    this.loaded = true
                }
            }
        }
    }))

    // Dropdown Component
    Alpine.data('dropdown', () => ({
        open: false,

        toggle() {
            this.open = !this.open
        },

        close() {
            this.open = false
        }
    }))

    // Modal Component
    Alpine.data('modal', () => ({
        open: false,

        init() {
            this.$watch('open', value => {
                document.body.classList.toggle('overflow-hidden', value)
            })
        },

        toggle() {
            this.open = !this.open
        },

        close() {
            this.open = false
        }
    }))

    // Accordion Component
    Alpine.data('accordion', () => ({
        active: null,

        toggle(index) {
            this.active = this.active === index ? null : index
        },

        isOpen(index) {
            return this.active === index
        }
    }))

    // Tabs Component
    Alpine.data('tabs', () => ({
        activeTab: 0,

        setTab(index) {
            this.activeTab = index
        },

        isActive(index) {
            return this.activeTab === index
        }
    }))

    // Compare Cars Component
    Alpine.data('carCompare', () => ({
        cars: [],
        maxCars: 3,

        add(car) {
            if (this.cars.length >= this.maxCars) {
                return false
            }
            if (!this.cars.find(c => c.id === car.id)) {
                this.cars.push(car)
                return true
            }
            return false
        },

        remove(carId) {
            this.cars = this.cars.filter(c => c.id !== carId)
        },

        clear() {
            this.cars = []
        },

        get count() {
            return this.cars.length
        },

        get isFull() {
            return this.cars.length >= this.maxCars
        }
    }))

    // Favorites/Wishlist Component
    Alpine.data('favorites', () => ({
        items: JSON.parse(localStorage.getItem('favorites') || '[]'),

        toggle(carId) {
            const index = this.items.indexOf(carId)
            if (index === -1) {
                this.items.push(carId)
            } else {
                this.items.splice(index, 1)
            }
            this.save()
        },

        has(carId) {
            return this.items.includes(carId)
        },

        save() {
            localStorage.setItem('favorites', JSON.stringify(this.items))
        },

        clear() {
            this.items = []
            this.save()
        }
    }))

    // Dark Mode Toggle
    Alpine.data('darkMode', () => ({
        enabled: false,

        init() {
            // Check local storage or system preference
            const saved = localStorage.getItem('darkMode')
            if (saved !== null) {
                this.enabled = saved === 'true'
            } else {
                this.enabled = window.matchMedia('(prefers-color-scheme: dark)').matches
            }
            this.update()
        },

        toggle() {
            this.enabled = !this.enabled
            this.update()
        },

        update() {
            document.documentElement.classList.toggle('dark', this.enabled)
            localStorage.setItem('darkMode', this.enabled)
        }
    }))

    // Infinite Scroll / Load More
    Alpine.data('loadMore', (fetchUrl) => ({
        items: [],
        page: 1,
        loading: false,
        hasMore: true,
        url: fetchUrl,

        async load() {
            if (this.loading || !this.hasMore) return

            this.loading = true

            try {
                const response = await fetch(`${this.url}?page=${this.page}`)
                const data = await response.json()

                this.items.push(...data.items)
                this.hasMore = data.hasMore
                this.page++
            } catch (error) {
                console.error('Failed to load more items:', error)
            } finally {
                this.loading = false
            }
        }
    }))
})

// Utility Functions
const AutoMaroc = {
    // Format price in MAD currency
    formatPrice(price) {
        return new Intl.NumberFormat('fr-MA', {
            style: 'currency',
            currency: 'MAD',
            minimumFractionDigits: 0
        }).format(price)
    },
    
    // Format number with separators
    formatNumber(num) {
        return new Intl.NumberFormat('fr-MA').format(num)
    },
    
    // Debounce function for search inputs
    debounce(func, wait) {
        let timeout
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout)
                func(...args)
            }
            clearTimeout(timeout)
            timeout = setTimeout(later, wait)
        }
    },
    
    // Copy text to clipboard
    async copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text)
            return true
        } catch (err) {
            console.error('Failed to copy:', err)
            return false
        }
    },
    
    // Share car via WhatsApp
    shareViaWhatsApp(carTitle, carUrl, phone) {
        const text = encodeURIComponent(`Bonjour! Je suis intéressé par cette voiture: ${carTitle}\n${carUrl}`)
        window.open(`https://wa.me/${phone}?text=${text}`, '_blank')
    }
}

// Make AutoMaroc available globally
window.AutoMaroc = AutoMaroc

// DOM Ready - Initialize any vanilla JS components
document.addEventListener('DOMContentLoaded', () => {
    // Add smooth scroll behavior
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault()
            const target = document.querySelector(this.getAttribute('href'))
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                })
            }
        })
    })
    
    // Initialize tooltips if any
    const tooltipTriggers = document.querySelectorAll('[data-tooltip]')
    tooltipTriggers.forEach(trigger => {
        trigger.addEventListener('mouseenter', (e) => {
            // Tooltip logic here if needed
        })
    })
})
