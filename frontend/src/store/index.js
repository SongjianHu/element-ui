import { createStore } from 'vuex'
import api from '@/api'

export default createStore({
  state: {
    suppliers: [],
    categories: [],
    products: [],
    purchaseOrders: [],
    inventory: [],
    loading: false,
    error: null
  },
  
  mutations: {
    SET_LOADING(state, loading) {
      state.loading = loading
    },
    SET_ERROR(state, error) {
      state.error = error
    },
    SET_SUPPLIERS(state, suppliers) {
      state.suppliers = suppliers
    },
    SET_CATEGORIES(state, categories) {
      state.categories = categories
    },
    SET_PRODUCTS(state, products) {
      state.products = products
    },
    SET_PURCHASE_ORDERS(state, orders) {
      state.purchaseOrders = orders
    },
    SET_INVENTORY(state, inventory) {
      state.inventory = inventory
    }
  },
  
  actions: {
    async fetchSuppliers({ commit }) {
      commit('SET_LOADING', true)
      try {
        const response = await api.get('/suppliers/')
        commit('SET_SUPPLIERS', response.data)
      } catch (error) {
        commit('SET_ERROR', error.message)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchCategories({ commit }) {
      commit('SET_LOADING', true)
      try {
        const response = await api.get('/categories/')
        commit('SET_CATEGORIES', response.data)
      } catch (error) {
        commit('SET_ERROR', error.message)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchProducts({ commit }) {
      commit('SET_LOADING', true)
      try {
        const response = await api.get('/products/')
        commit('SET_PRODUCTS', response.data)
      } catch (error) {
        commit('SET_ERROR', error.message)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchPurchaseOrders({ commit }) {
      commit('SET_LOADING', true)
      try {
        const response = await api.get('/purchase-orders/')
        commit('SET_PURCHASE_ORDERS', response.data)
      } catch (error) {
        commit('SET_ERROR', error.message)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchInventory({ commit }) {
      commit('SET_LOADING', true)
      try {
        const response = await api.get('/inventory/')
        commit('SET_INVENTORY', response.data)
      } catch (error) {
        commit('SET_ERROR', error.message)
      } finally {
        commit('SET_LOADING', false)
      }
    }
  },
  
  getters: {
    suppliers: state => state.suppliers,
    categories: state => state.categories,
    products: state => state.products,
    purchaseOrders: state => state.purchaseOrders,
    inventory: state => state.inventory,
    loading: state => state.loading,
    error: state => state.error
  }
}) 