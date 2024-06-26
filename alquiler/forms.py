from django import forms
from .models import ventaboletos, Persona,RolSalida

class RolSalidaForm(forms.ModelForm):
    hora_inicio = forms.TimeField(
        widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        label='Hora de Inicio'
    )
    hora_fin = forms.TimeField(
        widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        label='Hora de Finalizacion'
    )

    class Meta:
        model = RolSalida
        fields = ['nombre', 'hora_inicio', 'hora_fin', 'persona']
        
class RegistroForm(forms.ModelForm):
    class Meta:
        model = ventaboletos
        fields = ['persona', 'cliente', 'detalle', 'boleto', 'total', 'asiento']

    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)
        if 'persona' in self.data:
            try:
                persona_id = int(self.data.get('persona'))
                persona = Persona.objects.get(id=persona_id)
                categoria = persona.categoria
                asientos_ocupados = ventaboletos.objects.filter(persona__categoria=categoria).values_list('asiento', flat=True)
                asientos_disponibles = [i for i in range(1, categoria.asientos + 1) if i not in asientos_ocupados]
                self.fields['asiento'].choices = [(i, i) for i in asientos_disponibles]
            except (ValueError, TypeError, Persona.DoesNotExist):
                pass
        else:
            self.fields['asiento'].choices = []