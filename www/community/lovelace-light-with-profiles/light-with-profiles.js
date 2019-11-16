import { LitElement, html, css } from "https://unpkg.com/lit-element@2.0.1/lit-element.js?module";

class LightWithProfiles extends LitElement {
  static get properties() {
    return {
      hass: {},
      config: {}
    };
  }

  constructor() {
    super();

    this.lightProfiles = {};
  }

  render() {
    return html`
      <ha-card>
        ${this.config.title ? html`
          <div class="card-header">
            <div class="name">${this.config.title}</div>
            </div>
        ` : ''}
        <div class="card-content entities">
          ${this.config.entities.map(ent => {
            const stateObj = this.hass.states[ent.entity];
            return stateObj
              ? html`
                  <span class="label">${stateObj.attributes.friendly_name}</span>
                  <div class="profiles">
                    ${ent.profiles ? ent.profiles.map(profile => {
                      return html`
                        <ha-icon class="profile-icon"
                          ?active="${this.profileClass(stateObj, profile.name)}"
                          .icon="${profile.icon}"
                          .title="${profile.name}"
                          @click="${() => this.turnOnProfile(ent.entity, profile.name)}"
                        ></ha-icon>
                      `;
                    }) : ''}
                  </div>
                  <ha-switch
                    ?checked="${stateObj.state === 'on'}"
                    @click="${() => this.toggleLight(ent.entity)}"
                  ></ha-switch>
                `
              : 'Entity not found!';
          })}
        </div>
      </ha-card>
    `;
  }

  toggleLight(entity) {
    this.hass.callService("homeassistant", "toggle", {
      entity_id: entity
    });
  }

  turnOnProfile(entity, pro) {
    if (entity == 'light.keuken_werk') {
      switch(pro) {	
        case 'overdag':
          var color_temp = 263;
          var brightness_pct = 94;
          break;
        case 'avond':
          var color_temp = 403;
          var brightness_pct = 81;
          break;
        case 'relax':
          var color_temp = 427;
          var brightness_pct = 50;
          break;
      }
      this.hass.callService('script', 'turn_on_ikea_light_color_temp', {
        'entity_id': entity,
        'brightness_pct': brightness_pct,
        'color_temp': color_temp
      })
		} else if (entity == 'light.livingcolors') {
			switch(pro) {	
        case 'overdag':
          var brightness = 97;
					var transition = 5;
					var xy_color = [0.492, 0.474]
          break;
        case 'avond':
          var brightness = 131;
					var transition = 5;
					var xy_color = [0.508, 0.451]
          break;
        case 'relax':
          var brightness = 35;
					var transition = 5;
					var xy_color = [0.582, 0.395]
          break;
      }
			this.hass.callService('light', 'turn_on', {
				'entity_id': entity,
				'brightness': brightness,
				'transition': transition,
				'xy_color': xy_color
			})
    } else {
			switch(entity) {
				case 'light.av_meubel':
					switch(pro) {
						case 'overdag':
							var brightness_pct = 94
							var r = 255
							var g = 205
							var b = 122
							break;
						case 'avond':
							var brightness_pct = 80
							var r = 255
							var g = 170
							var b = 88
							break;
						case 'relax':
							var brightness_pct = 22
							var r = 255
							var g = 149
							var b = 50
							break;
					}
				case 'light.bureau':
					switch(pro) {
						case 'overdag':
							var brightness_pct = 94
							var r = 255
							var g = 205
							var b = 122
							break;
						case 'avond':
							var brightness_pct = 63
							var r = 255
							var g = 149
							var b = 50
							break;
						case 'relax':
							var brightness_pct = 11
							var r = 255
							var g = 96
							var b = 0
							break;
					}
			}
      this.hass.callService('script', 'turn_on_ikea_light_rgb_color', {
        'entity_id': entity,    
        'brightness_pct': brightness_pct,
        'r': r,
        'g': g,
        'b': b
      })
    };
  }

  profileClass(stateObj, profile) {
    if (stateObj.attributes.xy_color && stateObj.attributes.brightness) {
      const activeProfile = `${stateObj.attributes.xy_color.toString()},${stateObj.attributes.brightness.toString()}`;

      if (activeProfile === this.lightProfiles[profile]) {
        return true;
      }
    }

    return false;
  }

  setConfig(config) {
    if (!config.entities) {
      throw new Error("You need to define entities");
    }

    const ll = this.getLovelace();

    if (ll.config && ll.config.light_profiles) {
      this.lightProfiles = ll.config.light_profiles;
    }

    this.config = config;
  }

  getCardSize() {
    return this.config.entities.length + 1;
  }

  static get styles() {
    return css`
      .entities {
        display: grid;
        grid-template-columns: auto auto 46px;
        gap: 16px 10px;
        margin-top: 8px;
      }

      .label {
        font-size: 1.2rem;
        font-weight: 500;
      }

      .profiles {
        display: flex;
        flex-direction: row;
        flex-wrap: nowrap;
        justify-content: space-around;
        align-content: stretch;
        align-items: flex-start;
      }

      .profile-icon {
        cursor: pointer;
        fill: var(--disabled-text-color);
      }

      .profile-icon[active] {
        fill: var(--primary-color);
      }

      ha-switch {
        cursor: pointer;
      }
    `;
  }
  // https://github.com/custom-cards/custom-card-helpers/blob/master/src/get-lovelace.ts
  getLovelace() {
    let root = document.querySelector('home-assistant');
    root = root && root.shadowRoot;
    root = root && root.querySelector('home-assistant-main');
    root = root && root.shadowRoot;
    root = root && root.querySelector('app-drawer-layout partial-panel-resolver');
    root = root && root.shadowRoot || root;
    root = root && root.querySelector('ha-panel-lovelace');
    root = root && root.shadowRoot;
    root = root && root.querySelector('hui-root');
    if (root) {
        const ll = root.lovelace;
        ll.current_view = root.___curView;
        return ll;
    }
    return null;
  }
}

customElements.define('light-with-profiles', LightWithProfiles);
