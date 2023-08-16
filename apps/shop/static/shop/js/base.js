// ------------------------------------------------------------
// ref
// ------------------------------------------------------------

const Component = (data) => {
  if (typeof data["el"] === "string") {
    data["el"] = $(data["el"]);
  }

  if ("init" in data) {
    data.init();
  }
  return data;
};

// ------------------------------------------------------------
// EventBus
// ------------------------------------------------------------

const EventBus = {
  _eventTarget: new EventTarget(),

  subscribe(eventName, callback) {
    this._eventTarget.addEventListener(eventName, callback);
  },
  publish(eventName, detail) {
    const event = new CustomEvent(eventName, {
      detail,
    });
    this._eventTarget.dispatchEvent(event);
  },
  unsubscribe(eventName, callback) {
    this._eventTarget.removeEventListener(eventName, callback);
  },
};

// ------------------------------------------------------------
// Store
// ------------------------------------------------------------

/**
 * Creates a store
 * @param {
 *      data: object,
 *      listeners: object,
 *      computed: object,
 *      actions: object,
 *      getters: object,
 *      setters: object,
 *      init: function,
 * } initialState
 *
 * Listeners must be called like data attributes, and must be and array of functions.
 * */
function CreateStore(initialState) {
  let listeners = "listeners" in initialState ? initialState["listeners"] : {};
  let computed = "computed" in initialState ? initialState["computed"] : {};

  let state = {
    data: initialState["data"] || {},
    actions: initialState["actions"] || {},
    getters: initialState["getters"] || {},
    setters: initialState["setters"] || {},
  };

  // Data
  // ------------------------------------------------------------
  const proxyHandler = {
    get(target, key) {
      if (key in computed) {
        return computed[key];
      }

      if (key in target) {
        return target[key];
      }

      throw new ReferenceError(`Property ${key} does not exist in the store`);
    },
    set(target, key, value) {
      if (value !== target[key]) {
        target[key] = value;

        if (key in listeners) {
          listeners[key].forEach((listener) => listener(target, state.actions));
        }

        if (computed.length > 0) {
          for (const computedKey in computed) {
            target[computedKey] = computed[computedKey](target);
          }
        }
      }

      return true;
    },
  };

  if (!("data" in initialState)) {
    throw new ReferenceError("The store must have a data property");
  }

  state.data = new Proxy(initialState["data"], proxyHandler);

  // Actions
  // ------------------------------------------------------------
  for (const key in initialState.actions) {
    state.actions[key] = initialState.actions[key].bind(null, state.data, state.actions);
  }

  // Getters
  // ------------------------------------------------------------

  for (const key in initialState.getters) {
    state.getters[key] = initialState.getters[key].bind(null, state.data);
  }

  // Setters
  // ------------------------------------------------------------

  for (const key in initialState.setters) {
    state.setters[key] = (value) => {
      initialState.setters[key](state.data, value);
    };
  }

  // ------------------------------------------------------------
  const _state = {
    getState() {
      return state;
    },
    addComputed(key, computedFn) {
      computed[key] = computedFn;
      state.data[key] = computedFn(state.data);
    },
    subscribe(key, listener) {
      if (!listeners[key]) {
        listeners[key] = [];
      }

      listeners[key].push(listener);

      return () => {
        const index = listeners[key].indexOf(listener);
        listeners[key].splice(index, 1);
      };
    },
    dispatch(key, detail) {
      if (listeners[key]) {
        listeners[key].forEach((listener) => listener(state.data, detail));
      }
    },
  };

  if ("init" in initialState) {
    _state.init = initialState.init(state);
  }

  return _state;
}

// ------------------------------------------------------------
// Alert
// ------------------------------------------------------------

function AlertFactory(target) {
  const targetElement = $(target);
  const alertClass = "rounded-sm shadow-lg p-2";
  const successClass = "text-green-500 bg-green-200";
  const errorClass = "text-red-500 bg-red-200";
  const warningClass = "text-yellow-500 bg-yellow-200";
  const infoClass = "text-blue-500 bg-blue-200";

  const state = {
    el: targetElement,
    alertClass,
    successClass,
    errorClass,
    warningClass,
    infoClass,
    init() {
      this.hide();
      this.el.click(() => this.hide());
      this.el.addClass(this.alertClass);
    },
    resetClass() {
      this.el.removeClass(this.successClass);
      this.el.removeClass(this.errorClass);
      this.el.removeClass(this.warningClass);
      this.el.removeClass(this.infoClass);
    },
    hide() {
      this.el.hide();
    },
    show(info) {
      this.el.text(info);
      this.el.show();
    },
    error(info) {
      this.resetClass();
      this.el.addClass(this.errorClass);
      this.show(info);
    },
    success(info) {
      this.resetClass();
      this.el.addClass(this.successClass);
      this.show(info);
    },
    warning(info) {
      this.resetClass();
      this.el.addClass(this.warningClass);
      this.show(info);
    },
    info(info) {
      this.resetClass();
      this.el.addClass(this.infoClass);
      this.show(info);
    },
  };

  state.init();

  return state;
}

// const AlertFactory = Comment({
//   el: $("#alert"),
//   successClass: "text-green-500 bg-green-200",
//   errorClass: "text-red-500 bg-red-200",
//   init() {
//     this.hidden();
//     this.el.click(() => this.hidden());

//     EventBus.subscribe("alert-error", (e) => {
//       this.showError(e.detail);
//     });
//     EventBus.subscribe("alert-success", (e) => {
//       this.showSuccess(e.detail);
//     });
//   },
//   hidden() {
//     this.el.hide();
//   },
//   show(info) {
//     this.el.text(info);
//     this.el.show();
//   },
//   showError(info) {
//     this.el.removeClass(this.successClass);
//     this.el.addClass(this.errorClass);
//     this.show(info);
//   },
//   showSuccess(info) {
//     this.el.removeClass(this.errorClass);
//     this.el.addClass(this.successClass);
//     this.show(info);
//   },
// });
