loaded_forms = {
    
    'login_form': [
        {'html': '\n'
          '    <div class="field-group">\n'
          '        <label for="id_email">Email:</label>\n'
          '        <input type="text" name="email" id="id_email" '
          'placeholder="Digite seu email" inputmode="email">\n'
          '        \n'
          '        <div class="error"></div>\n'
          '    </div>\n'
          '    ',
        'name': 'email'},
        {'html': '\n'
                '    <div class="field-group">\n'
                '        <label for="id_password">Senha:</label>\n'
                '        <input type="password" name="password" id="id_password" '
                'placeholder="Digite sua senha">\n'
                '        <div class="block-forgot-password"><a href="/nova-senha/informar-email">Esqueceu a '
                'senha?</a></div>\n'
                '        <div class="error"></div>\n'
                '    </div>\n'
                '    ',
        'name': 'password'}
    ],
    
    'fast_login_form': """
            <div class="field-group">
            <label for="id_email">Email:</label>
            <input type="text" name="email" id="id_email" placeholder="Digite seu email" inputmode="email">

            <div class="error"></div>
        </div>

        <div class="field-group">
            <label for="id_password">Senha:</label>
            <input type="password" name="password" id="id_password" placeholder="Digite sua senha">
            <div class="block-forgot-password"><a href="/nova-senha/informar-email">Esqueceu a senha?</a></div>
            <div class="error"></div>
        </div>
    """,
    
    'register_form':[
      {'html': '\n'
                '        <div class="field-group">\n'
                '            <label for="id_name">Nome:</label>\n'
                '            <input type="text" name="name" id="id_name" '
                'placeholder="Digite seu nome">\n'
                '            <div class="error"></div>\n'
                '        </div>\n'
                '    ',
        'name': 'name'},
      {'html': '\n'
                '        <div class="field-group">\n'
                '            <label for="id_email">Email:</label>\n'
                '            <input type="text" name="email" id="id_email" '
                'placeholder="Digite seu email" inputmode="email">\n'
                '            <div class="error"></div>\n'
                '        </div>\n'
                '    ',
        'name': 'email'},
      {'html': '\n'
                '        <div class="field-group">\n'
                '            <label for="id_password">Senha:</label>\n'
                '            <input type="password" name="password" id="id_password" '
                'placeholder="Digite sua senha">\n'
                '            <div class="error"></div>\n'
                '        </div>\n'
                '    ',
        'name': 'password'},
      {'html': '\n'
                '        <div class="field-group">\n'
                '            <label for="id_confirm_password">Confirmar '
                'senha:</label>\n'
                '            <input type="password" name="confirm_password" '
                'id="id_confirm_password" placeholder="Confirme sua senha">\n'
                '            <div class="error"></div>\n'
                '        </div>\n'
                '    ',
        'name': 'confirm_password'}
      ],
    
    'fast_register_form': """
            <div class="field-group">
            <label for="id_name">Nome:</label>
            <input type="text" name="name" id="id_name" placeholder="Digite seu nome">
            <div class="error"></div>
        </div>

        <div class="field-group">
            <label for="id_email">Email:</label>
            <input type="text" name="email" id="id_email" placeholder="Digite seu email" inputmode="email">
            <div class="error"></div>
        </div>

        <div class="field-group">
            <label for="id_password">Senha:</label>
            <input type="password" name="password" id="id_password" placeholder="Digite sua senha">
            <div class="error"></div>
        </div>

        <div class="field-group">
            <label for="id_confirm_password">Confirmar senha:</label>
            <input type="password" name="confirm_password" id="id_confirm_password" placeholder="Confirme sua senha">
            <div class="error"></div>
        </div>
    """,
    
    'password_form': [
        {'html': '\n'
                  '    <div class="ag-form-group">\n'
                  '        <label for="current_password" class="ag-label">Senha '
                  'atual:</label>\n'
                  '        <input type="password" name="current_password" '
                  'id="id_current_password" class="input" placeholder="Digite sua '
                  'senha atual">\n'
                  '        <div class="error"></div>\n'
                  '    </div>\n'
                  '    ',
          'name': 'current_password'},
        {'html': '\n'
                  '    <div class="ag-form-group">\n'
                  '        <label for="new_password" class="ag-label">Nova '
                  'senha:</label>\n'
                  '        <input type="password" name="new_password" '
                  'id="id_new_password" class="input" placeholder="Digite sua nova '
                  'senha">\n'
                  '        <div class="error"></div>\n'
                  '    </div>\n'
                  '    ',
          'name': 'new_password'},
        {'html': '\n'
                  '    <div class="ag-form-group">\n'
                  '        <label for="confirm_new_password" '
                  'class="ag-label">Confirmar senha:</label>\n'
                  '        <input type="password" name="confirm_new_password" '
                  'id="id_confirm_new_password" class="input" placeholder="Corfirme '
                  'sua nova senha">\n'
                  '        <div class="error"></div>\n'
                  '    </div>\n'
                  '    ',
          'name': 'confirm_new_password'}
      ],
    
    'fast_password_form': """
        <div class="ag-form-group">
          <label for="current_password" class="ag-label">Senha atual:</label>
          <input type="password" name="current_password" id="id_current_password" class="input" placeholder="Digite sua senha atual">
          <div class="error"></div>
        </div>
        <div class="ag-form-group">
            <label for="new_password" class="ag-label">Nova senha:</label>
            <input type="password" name="new_password" id="id_new_password" class="input" placeholder="Digite sua nova senha">
            <div class="error"></div>
        </div>
        <div class="ag-form-group">
            <label for="confirm_new_password" class="ag-label">Confirmar senha:</label>
            <input type="password" name="confirm_new_password" id="id_confirm_new_password" class="input" placeholder="Confirme sua nova senha">
            <div class="error"></div>
        </div>
    """

    
}