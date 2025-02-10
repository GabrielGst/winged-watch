// FYI : https://github.com/tailwindlabs/tailwindcss-forms


export default function InputLabel({ form, type, id, placeholder }: {form: string, type: string, id: string, placeholder: string}) {
  return (
    /*
      Heads up! 👋

      Plugins:
        - @tailwindcss/forms
    */

    <label
      htmlFor={`${id}`}
      form={`${form}`}
      className="relative block overflow-hidden rounded-md border border-gray-200 px-3 pt-3 shadow-xs focus-within:border-blue-600 focus-within:ring-1 focus-within:ring-blue-600"
    >
      <input
        type={`${type}`}
        id={`${id}`}
        placeholder={`${placeholder}`}
        className="peer h-8 w-full border-none bg-transparent p-0 placeholder-transparent focus:border-transparent focus:ring-0 focus:outline-hidden sm:text-sm"
      />

      <span
        className="absolute start-3 top-3 -translate-y-1/2 text-xs text-gray-700 transition-all peer-placeholder-shown:top-1/2 peer-placeholder-shown:text-sm peer-focus:top-3 peer-focus:text-xs"
      >
        {type}
      </span>
    </label>
  );
}